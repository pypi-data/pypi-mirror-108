from datetime import datetime
import os
from pathlib import Path
import platform
import subprocess
import sys
from typing import Any, Callable, Dict, List, Optional, Tuple
from unittest.mock import ANY, Mock

import pytest
import requests
import yaml

import anyscale
from anyscale.client.openapi_client.models.app_config import AppConfig
from anyscale.client.openapi_client.models.build import Build
from anyscale.client.openapi_client.models.project import Project
from anyscale.client.openapi_client.models.project_response import ProjectResponse
from anyscale.client.openapi_client.models.session import Session
from anyscale.connect import (
    _is_in_shell,
    ClientBuilder,
    PINNED_IMAGES,
    REQUIRED_RAY_COMMIT,
    REQUIRED_RAY_VERSION,
)
from anyscale.util import get_wheel_url
import anyscale.utils.runtime_env


def _make_session(i: int, state: str) -> Session:
    sess = Session(
        id="session_id",
        name="cluster-{}".format(i),
        created_at=datetime.now(),
        snapshots_history=[],
        idle_timeout=120,
        tensorboard_available=False,
        project_id="project_id",
        state=state,
        service_proxy_url="http://session-{}.userdata.com/auth?token=value&bar".format(
            i
        ),
        connect_url="session-{}.userdata.com:8081?port=10001".format(i),
        jupyter_notebook_url="http://session-{}.userdata.com/jupyter/lab?token=value".format(
            i
        ),
        access_token="value",
    )
    sess.build_id = "build_id"
    sess.compute_template_id = "mock_compute_template_id"
    return sess


def _make_app_template() -> AppConfig:
    return AppConfig(
        project_id="project_id",
        id="application_template_id",
        name="test-app-config",
        creator_id="creator_id",
        created_at=datetime.now(),
        last_modified_at=datetime.now(),
    )


def _make_build() -> Build:
    return Build(
        id="build_id",
        revision=0,
        application_template_id="application_template_id",
        config_json="",
        creator_id="creator_id",
        status="succeeded",
        created_at=datetime.now(),
        last_modified_at=datetime.now(),
        docker_image_name="docker_image_name",
    )


def _connected(ray: Mock, ret: Dict[str, Any],) -> Callable[[Any, Any], Dict[str, Any]]:
    def connected(*a: Any, **kw: Any) -> Dict[str, Any]:
        ray.util.client.ray.is_connected.return_value = True
        returnable = {
            "num_clients": 1,
            "ray_version": REQUIRED_RAY_VERSION,
            "ray_commit": REQUIRED_RAY_COMMIT,
            "python_version": platform.python_version(),
        }
        returnable.update(**ret)
        return returnable

    return connected


def _make_test_builder(
    tmp_path: Path,
    session_states: Optional[List[str]] = None,
    setup_project_dir: bool = True,
    create_build: bool = True,
) -> Tuple[Any, Any, Any, Any]:
    if session_states is None:
        session_states = ["Running"]

    scratch = tmp_path / "scratch"
    sdk = Mock()
    sess_resp = Mock()
    ray = Mock()

    ray.__commit__ = REQUIRED_RAY_COMMIT
    ray.__version__ = REQUIRED_RAY_VERSION
    ray.util.client.ray.is_connected.return_value = False
    anyscale.utils.runtime_env.runtime_env_setup = Mock()

    def disconnected(*a: Any, **kw: Any) -> None:
        ray.util.client.ray.is_connected.return_value = False

    # Emulate session lock failure.
    ray.util.connect.side_effect = _connected(ray, {"num_clients": 1})
    ray.util.disconnect.side_effect = disconnected
    job_config_mock = Mock()
    job_config_mock.runtime_env = {}
    job_config_mock.set_runtime_env.return_value = Mock()
    job_config_mock.metadata = {}
    ray.job_config.JobConfig.return_value = job_config_mock
    sess_resp.results = [
        _make_session(i, state) for i, state in enumerate(session_states)
    ]
    sess_resp.metadata.next_paging_token = None
    sdk.list_sessions.return_value = sess_resp
    proj_resp = Mock()
    proj_resp.result.name = "scratch"
    sdk.get_project.return_value = proj_resp
    subprocess = Mock()
    _os = Mock()
    _api_client = Mock()
    _api_client.get_user_info_api_v2_userinfo_get.return_value.result = Mock(
        organizations=[Mock(default_cloud_id=None)]
    )
    builder = ClientBuilder(
        scratch_dir=scratch.absolute().as_posix(),
        anyscale_sdk=sdk,
        subprocess=subprocess,
        _ray=ray,
        _os=_os,
        _ignore_version_check=False,
        api_client=_api_client,
    )
    if setup_project_dir:
        builder.project_dir(scratch.absolute().as_posix())
    else:
        builder._in_shell = True
    builder._find_project_id = lambda _: None  # type: ignore

    def create_session(*a: Any, **kw: Any) -> None:
        sess_resp.results = sess_resp.results + [
            _make_session(len(sess_resp.results), "Running")
        ]
        sdk.list_sessions.return_value = sess_resp

    setattr(builder, "_start_session", Mock())
    builder._start_session.side_effect = create_session  # type: ignore
    builder._register_compute_template = Mock(return_value="mock_compute_template_id")  # type: ignore

    setattr(
        builder, "_get_last_used_cloud", Mock(return_value="anyscale_default_cloud")
    )

    if create_build:
        _make_app_template()
        mock_build = _make_build()
        builder._get_cluster_env_build = Mock(return_value=mock_build)  # type: ignore

    return builder, sdk, subprocess, ray


def test_parse_address() -> None:
    """Tests ClientBuilder._parse_address which parses the anyscale address."""

    sdk = Mock()
    _api_client = Mock()
    connect_instance = ClientBuilder(anyscale_sdk=sdk, api_client=_api_client)

    connect_instance._parse_address(None)
    assert connect_instance._cluster_name is None
    assert connect_instance._autosuspend_timeout == 120
    assert connect_instance._cluster_compute_name is None
    assert connect_instance._cluster_env_name is None

    connect_instance._parse_address("")
    assert connect_instance._cluster_name is None
    assert connect_instance._autosuspend_timeout == 120
    assert connect_instance._cluster_compute_name is None
    assert connect_instance._cluster_env_name is None

    connect_instance._parse_address("cluster_name")
    assert connect_instance._cluster_name == "cluster_name"
    assert connect_instance._autosuspend_timeout == 120
    assert connect_instance._cluster_compute_name is None
    assert connect_instance._cluster_env_name is None

    connect_instance._parse_address(
        "my_cluster?cluster_compute=my_template&autosuspend=5&cluster_env=bla:1&update=True"
    )
    assert connect_instance._cluster_name == "my_cluster"
    assert connect_instance._autosuspend_timeout == 5
    assert connect_instance._cluster_compute_name == "my_template"
    assert connect_instance._cluster_env_name == "bla"
    assert connect_instance._needs_update

    with pytest.raises(ValueError):
        # we only support cluster_compute, cluster_env, autosuspend
        connect_instance._parse_address("my_cluster?random=5")


def test_new_proj_connect_params(tmp_path: Path, project_test_data: Project) -> None:
    project_dir = (tmp_path / "my_proj").absolute().as_posix()
    builder, sdk, _, ray = _make_test_builder(tmp_path)
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should create a new .anyscale.yaml file
    builder.project_dir(project_dir).connect()

    assert anyscale.project.get_project_id(project_dir)
    builder._start_session.assert_called_once_with(
        project_id=project_test_data.id,
        cluster_name="cluster-1",
        build_id="build_id",
        compute_template_id="mock_compute_template_id",
    )

    # Also check connection params in this test.
    ray.util.connect.assert_called_with(
        "session-1.userdata.com:8081",
        metadata=[("cookie", "anyscale-token=value"), ("port", "10001")],
        secure=False,
        connection_retries=10,
        ignore_version=True,
        job_config=ray.job_config.JobConfig(),
    )


def test_detect_existing_proj(tmp_path: Path) -> None:
    nested_dir = (tmp_path / "my_proj" / "nested").absolute().as_posix()
    parent_dir = os.path.dirname(nested_dir)
    os.makedirs(nested_dir)
    builder, _, _, _ = _make_test_builder(tmp_path, [], setup_project_dir=False)

    # Setup project in parent dir
    project_yaml = os.path.join(parent_dir, ".anyscale.yaml")
    with open(project_yaml, "w+") as f:
        f.write(yaml.dump({"project_id": 12345}))

    # Should detect the parent project dir
    cwd = os.getcwd()
    try:
        os.chdir(nested_dir)
        builder.session("cluster-0").connect()
    finally:
        os.chdir(cwd)

    builder._start_session.assert_called_once_with(
        project_id=ANY,
        cluster_name="cluster-0",
        build_id="build_id",
        compute_template_id="mock_compute_template_id",
    )


def test_fallback_scratch_dir(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, _, _ = _make_test_builder(tmp_path)
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should create a new .anyscale.yaml file in the scratch dir
    builder.connect()

    assert anyscale.project.get_project_id(scratch_dir)
    builder._start_session.assert_called_once_with(
        project_id=project_test_data.id,
        cluster_name="cluster-1",
        build_id="build_id",
        compute_template_id="mock_compute_template_id",
    )


def test_background_run_mode(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, _ = _make_test_builder(tmp_path)
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should create a new .anyscale.yaml file in the scratch dir
    builder.run_mode("background").connect()

    assert anyscale.project.get_project_id(scratch_dir)
    subprocess.check_output.assert_called_with(
        ["anyscale", "push", "cluster-1", "-s", ANY, "-t", ANY], stderr=ANY
    )
    subprocess.check_call.assert_called_with(ANY)
    builder._os._exit.assert_called_once_with(0)


def test_local_docker_run_mode(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, _ = _make_test_builder(tmp_path)
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should create a new .anyscale.yaml file in the scratch dir
    builder.run_mode("local_docker").connect()

    assert anyscale.project.get_project_id(scratch_dir)
    subprocess.check_call.assert_called_with(
        [
            "docker",
            "run",
            "--env",
            ANY,
            "--env",
            ANY,
            "-v",
            ANY,
            "--entrypoint=/bin/bash",
            ANY,
            "-c",
            ANY,
        ]
    )
    builder._os._exit.assert_called_once_with(0)


def test_connect_with_cloud(tmp_path: Path, project_test_data: Project) -> None:
    builder, sdk, _, _ = _make_test_builder(tmp_path, [])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should create a new .anyscale.yaml file in the scratch dir
    builder.session("cluster-0").cloud("test_cloud").connect()

    assert builder._cloud_name == "test_cloud"
    builder._start_session.assert_called_once_with(
        project_id=project_test_data.id,
        cluster_name="cluster-0",
        build_id="build_id",
        compute_template_id="mock_compute_template_id",
    )


def test_clone_scratch_dir(tmp_path: Path, project_test_data: Project) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, subprocess, _ = _make_test_builder(
        tmp_path, [], setup_project_dir=False
    )
    builder._find_project_id = lambda _: "foo"
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def clone_project(*a: Any, **kw: Any) -> None:
        os.makedirs(scratch_dir, exist_ok=True)
        project_yaml = os.path.join(scratch_dir, ".anyscale.yaml")
        with open(project_yaml, "w+") as f:
            f.write(yaml.dump({"project_id": 12345}))

    subprocess.check_call.side_effect = clone_project

    # Should create a new .anyscale.yaml file in the scratch dir
    builder.session("cluster-0").connect()

    subprocess.check_call.assert_called_once_with(["anyscale", "clone", "scratch"])
    builder._start_session.assert_called_once_with(
        project_id="12345",
        cluster_name="cluster-0",
        build_id="build_id",
        compute_template_id="mock_compute_template_id",
    )


def test_new_session(tmp_path: Path, project_test_data: Project) -> None:
    builder, sdk, _, _ = _make_test_builder(tmp_path, session_states=[])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should create a new session.
    builder.session("cluster-0").connect()

    builder._start_session.assert_called_once_with(
        project_id=ANY,
        cluster_name="cluster-0",
        build_id="build_id",
        compute_template_id="mock_compute_template_id",
    )


def test_reconnect_without_cluster_env(
    tmp_path: Path, project_test_data: Project
) -> None:
    """
    Tests the following situations to check the default cluster env logic:
    1. connect without any cluster env uses the default cluster env.
    2. Reconnect to existing terminated cluster without providing cluster env should use default
       cluster env even if previously the terminated cluster had a custom cluster env.
    3. Reconnect to existing terminated cluster and provide cluster env should use the
       provided cluster env.
    4. Connecting to an existing session never calls start.
    """
    builder, sdk, _, _ = _make_test_builder(tmp_path, session_states=[])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Create new session without providing cluster env. The default app config should be used
    # to start the cluster.
    builder.connect()
    builder._get_cluster_env_build.assert_called_once_with(
        "project_id", "default_app_config_1.4-rc2_py3" + str(sys.version_info[1]), None
    )
    builder._start_session.assert_called_once_with(
        project_id=ANY,
        cluster_name="cluster-0",
        build_id="build_id",
        compute_template_id="mock_compute_template_id",
    )

    # Terminate the cluster. Reconnect to same cluster without providing cluster env.
    # The cluster's cluster env should be the default one (not the one of the old terminated cluster).
    builder, sdk, _, _ = _make_test_builder(
        tmp_path, session_states=[], create_build=False,
    )
    session = _make_session(0, "Terminated")
    session.name = "cluster-0"
    session.build_id = "new_build_id"
    builder._get_session = Mock(return_value=session)
    mock_build = _make_build()
    sdk.get_build = Mock(return_value=Mock(result=mock_build))
    builder._get_cluster_env_build = Mock(return_value=mock_build)  # type: ignore
    builder.session("cluster-0").connect()

    # Terminate the cluster. Reconnect to same cluster and provide a new cluster env.
    # The cluster's cluster env should be the new one (not the one of the old terminated cluster).
    builder, sdk, _, _ = _make_test_builder(
        tmp_path, session_states=[], create_build=False,
    )
    session = _make_session(0, "Terminated")
    session.name = "cluster-0"
    session.build_id = "old_cluster_build_id"
    builder._get_session = Mock(return_value=session)
    mock_build = _make_build()
    mock_build.id = "newest_build_id"
    sdk.get_build = Mock(return_value=Mock(result=mock_build))
    builder._get_cluster_env_build = Mock(return_value=mock_build)  # type: ignore
    builder.session("cluster-0").cluster_env("newest_cluster_env_name").connect()
    builder._get_cluster_env_build.assert_called_once_with(
        "project_id", "newest_cluster_env_name", None
    )
    builder._start_session.assert_called_once_with(
        project_id=ANY,
        cluster_name="cluster-0",
        build_id="newest_build_id",
        compute_template_id="mock_compute_template_id",
    )

    # Reconnect to the same running cluster and provide a new cluster env.
    # The cluster should be untouched.
    builder, sdk, _, _ = _make_test_builder(
        tmp_path, session_states=[], create_build=False,
    )
    session = _make_session(0, "Running")
    session.name = "cluster-0"
    session.build_id = "old_cluster_build_id"
    builder._get_session = Mock(return_value=session)
    mock_build = _make_build()
    sdk.get_build = Mock(return_value=Mock(result=mock_build))
    builder._get_cluster_env_build = Mock(return_value=mock_build)  # type: ignore
    builder.session("cluster-0").cluster_env("random_name").connect()
    builder._start_session.assert_not_called()


def test_base_docker_image(tmp_path: Path, project_test_data: Project,) -> None:
    scratch_dir = (tmp_path / "scratch").absolute().as_posix()
    builder, _, _, _ = _make_test_builder(tmp_path, session_states=["Running"])

    # Base docker images are no longer supported
    with pytest.raises(ValueError):
        builder.project_dir(scratch_dir).base_docker_image(
            "anyscale/ray-ml:custom"
        ).connect()


def test_requirements_list(tmp_path: Path, project_test_data: Project) -> None:
    builder, _, _, _ = _make_test_builder(tmp_path, session_states=[])

    # anyscale.require().connect() no longer supported
    with pytest.raises(ValueError):
        builder.require(["pandas", "wikipedia"]).connect()


def test_new_session_lost_lock(tmp_path: Path, project_test_data: Project) -> None:
    builder, sdk, _, ray = _make_test_builder(tmp_path, session_states=[])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Emulate session lock failure.
    ray.util.connect.side_effect = _connected(ray, {"num_clients": 999999})

    # Should create a new session.
    with pytest.raises(RuntimeError):
        builder.connect()

    builder._start_session.assert_called_once_with(
        project_id=project_test_data.id,
        cluster_name="cluster-0",
        build_id="build_id",
        compute_template_id="mock_compute_template_id",
    )


def test_reuse_cluster_env_and_compute_match(
    tmp_path: Path, project_test_data: Project
) -> None:
    """ Checks that when the cluster is active, we never update it.
    TODO(ameer/IanR/Nikita): make cluster compute/env mismatch raise an error when Update=False.
    """
    (tmp_path / "scratch").absolute().as_posix()
    builder, sdk, _, ray = _make_test_builder(tmp_path)
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Create session to emulate build id match
    sess = _make_session(0, "Running")
    sess.build_id = "build_id"
    sess_resp = Mock()
    sess_resp.results = [sess]
    sess_resp.metadata.next_paging_token = None
    sdk.list_sessions.return_value = sess_resp

    # Build id doesn't match, does not update.
    # We do not update active clusters unless the user explicitly requests it.
    builder.session("cluster-0").connect()
    builder._start_session.assert_not_called()
    ray.util.disconnect()

    # Build id match, updated because the user explicitly asked for update.
    builder.session("cluster-0", update=True).connect()
    builder._start_session.assert_called_once_with(
        project_id=project_test_data.id,
        cluster_name="cluster-0",
        build_id="build_id",
        compute_template_id="mock_compute_template_id",
    )


def test_reuse_session_hash_mismatch(
    tmp_path: Path, project_test_data: Project
) -> None:
    """
    Checks that when the build id and compute template id don't match, a running session is
    updated with connect.
    """
    builder, sdk, _, _ = _make_test_builder(tmp_path)
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Emulate build id mismatch.
    sess = _make_session(0, "Running")
    sess.build_id = "wrong-build-id"
    sess_resp = Mock()
    sess_resp.results = [sess]
    sess_resp.metadata.next_paging_token = None
    sdk.list_sessions.return_value = sess_resp

    # Should connect and run 'start'.
    builder.session("cluster-0", update=True).connect()

    builder._start_session.assert_called_once_with(
        project_id=project_test_data.id,
        cluster_name="cluster-0",
        build_id="build_id",
        compute_template_id="mock_compute_template_id",
    )


def test_reuse_session_lock_failure(tmp_path: Path, project_test_data: Project) -> None:
    builder, sdk, _, ray = _make_test_builder(tmp_path, session_states=["Running"])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def create_session(*a: Any, **kw: Any) -> None:
        sess_resp = Mock()
        sess_resp.results = [
            _make_session(0, "Running"),
            _make_session(1, "Running"),
        ]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp
        ray.util.connect.side_effect = _connected(ray, {})

    builder._start_session.side_effect = create_session

    # Emulate session hash code match but lock failure.
    sess0 = _make_session(0, "Running")
    sess0.build_id = "build_id"
    sess1 = _make_session(0, "Running")
    sess1.build_id = "build_id"
    sess_resp = Mock()
    sess_resp.results = [sess0, sess1]
    sess_resp.metadata.next_paging_token = None
    sdk.list_sessions.return_value = sess_resp

    # Creates new session-1.
    builder.connect()

    builder._start_session.assert_called_once_with(
        project_id=project_test_data.id,
        cluster_name="cluster-1",
        build_id="build_id",
        compute_template_id="mock_compute_template_id",
    )


def test_restart_session_conn_failure(
    tmp_path: Path, project_test_data: Project
) -> None:
    builder, sdk, _, ray = _make_test_builder(tmp_path, session_states=["Running"])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def fail_first_session(url: str, *a: Any, **kw: Any) -> Any:
        raise ConnectionError("mock connect failure")

    # Emulate session hash code match but conn failure.
    ray.util.connect.side_effect = fail_first_session

    # Tries to restart it, but fails.
    with pytest.raises(ConnectionError):
        builder.connect()

    builder._start_session.assert_called_once_with(
        project_id=project_test_data.id,
        cluster_name="cluster-1",
        build_id="build_id",
        compute_template_id="mock_compute_template_id",
    )


def test_fixed_session(tmp_path: Path, project_test_data: Project) -> None:
    builder, sdk, _, _ = _make_test_builder(
        tmp_path, session_states=["Running", "Running"], create_build=False
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)
    mock_app_config = _make_app_template()
    mock_build = _make_build()
    mock_build.id = "mock_build_id"
    cluster_env_identifier = f"{mock_app_config.name}:{mock_build.revision}"
    builder._get_cluster_env_build = Mock(return_value=mock_build)  # type: ignore

    # Should connect and run 'up'.
    builder.session("cluster-1", update=True).cluster_env(
        cluster_env_identifier
    ).connect()

    builder._start_session.assert_called_once_with(
        project_id=project_test_data.id,
        cluster_name="cluster-1",
        build_id="mock_build_id",
        compute_template_id="mock_compute_template_id",
    )


def test_fixed_session_not_running(tmp_path: Path, project_test_data: Project,) -> None:
    builder, sdk, _, _ = _make_test_builder(
        tmp_path, session_states=["Running", "Stopped"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    # Should connect and run 'up'.
    builder.session("cluster-1").connect()

    builder._start_session.assert_called_once_with(
        project_id=project_test_data.id,
        cluster_name="cluster-1",
        build_id="build_id",
        compute_template_id="mock_compute_template_id",
    )


def test_fixed_session_static_ray_version_mismatch(
    tmp_path: Path, project_test_data: Project,
) -> None:
    builder, sdk, _, ray = _make_test_builder(
        tmp_path, session_states=["Running", "Stopped"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)
    ray.__commit__ = "fake_commit"

    # Should connect and not run 'up'.
    with pytest.raises(ValueError):
        builder.session("cluster-0").connect()

    builder._start_session.assert_not_called()


@pytest.mark.parametrize("remote_version_mismatch", [True, False])
def test_fixed_session_no_update(
    remote_version_mismatch: bool, tmp_path: Path, project_test_data: Project,
) -> None:
    builder, sdk, _, ray = _make_test_builder(
        tmp_path, session_states=["Running", "Running"]
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    if remote_version_mismatch:
        ray.util.connect.side_effect = _connected(ray, {"ray_commit": "bad commit"},)

    # Should connect and run 'up'.
    if remote_version_mismatch:
        with pytest.raises(ValueError):
            builder.session("cluster-1", update=False).connect()
    else:
        builder.session("cluster-1", update=False).connect()

    builder._start_session.assert_not_called()
    builder._ray.util.connect.assert_called_once()


def test_new_fixed_session(tmp_path: Path, project_test_data: Project) -> None:
    builder, sdk, _, _ = _make_test_builder(tmp_path, session_states=[])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    def create_session(*a: Any, **kw: Any) -> None:
        sess_resp = Mock()
        sess_resp.results = [_make_session(i, "Running") for i in range(3)]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp

    builder._start_session.side_effect = create_session

    # Should create a new session.
    builder.session("cluster-2").connect()

    builder._start_session.assert_called_once_with(
        project_id=project_test_data.id,
        cluster_name="cluster-2",
        build_id="build_id",
        compute_template_id="mock_compute_template_id",
    )


class MockPopen(object):
    def __init__(self) -> None:
        pass

    def communicate(self) -> Tuple[str, str]:
        return (
            '[{"id": "cloud2", "name": "second cloud"}, {"id": "cloud1", "name": "first cloud"}]',
            "",
        )


@pytest.mark.parametrize("org_default_cloud", [None, "mock_cloud_id"])
def test_get_default_cloud(
    org_default_cloud: Optional[str], tmp_path: Path, project_test_data: Project,
) -> None:
    subprocess = Mock()
    subprocess.Popen.return_value = MockPopen()
    sdk = Mock()
    project_test_data.last_used_cloud_id = None
    sdk.get_project.return_value = ProjectResponse(result=project_test_data)
    _api_client = Mock()
    _api_client.get_user_info_api_v2_userinfo_get.return_value.result = Mock(
        organizations=[Mock(default_cloud_id=org_default_cloud)]
    )
    _api_client.get_cloud_api_v2_clouds_cloud_id_get.return_value.result.name = (
        "mock_cloud_name"
    )
    builder = ClientBuilder(
        anyscale_sdk=sdk, subprocess=subprocess, api_client=_api_client
    )
    if org_default_cloud:
        # Check the correct default cloud is returned
        assert builder._get_organization_default_cloud() == "mock_cloud_name"
    else:
        # Check that we get the "default cloud" (cloud first created)
        # if there is no last used cloud.
        assert builder._get_last_used_cloud("prj_1") == "first cloud"
        project_test_data.last_used_cloud_id = "cloud2"
        # If there is a last used cloud, use that instead.
        assert builder._get_last_used_cloud("prj_1") == "second cloud"


@pytest.mark.parametrize("static_ray_version_mismatch", [True, False])
def test_cluster_env(
    static_ray_version_mismatch: bool, tmp_path: Path, project_test_data: Project,
) -> None:
    builder, sdk, _, ray = _make_test_builder(
        tmp_path, session_states=[], create_build=False
    )
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    if static_ray_version_mismatch:
        ray.__commit__ = "abcdef"
        ray.util.connect.side_effect = _connected(ray, {"ray_commit": "abcdef"},)

    app_templates_resp = Mock()
    app_templates_resp.results = [_make_app_template()]
    app_templates_resp.metadata.next_paging_token = None
    sdk.list_app_configs.return_value = app_templates_resp

    build = _make_build()
    builds_resp = Mock()
    builds_resp.results = [build]
    builds_resp.metadata.next_paging_token = None
    sdk.list_builds.return_value = builds_resp

    get_build_resp = Mock()
    get_build_resp.result = build
    sdk.get_build.return_value = get_build_resp

    def create_session(*a: Any, **kw: Any) -> None:
        sess_resp = Mock()
        sess_resp.results = [_make_session(0, "Running")]
        sess_resp.metadata.next_paging_token = None
        sdk.list_sessions.return_value = sess_resp

    builder._start_session.side_effect = create_session

    with pytest.raises(RuntimeError):
        builder.cluster_env("non-existent-app-config").connect()
    with pytest.raises(TypeError):
        builder.cluster_env([])

    builder.cluster_env(
        {"name": "my_custom_image", "base_image": "anyscale/ray-ml:pinned-nightly"}
    )
    assert builder._cluster_env_name == "my_custom_image"
    assert builder._cluster_env_dict == {"base_image": "anyscale/ray-ml:pinned-nightly"}
    builder.cluster_env({"base_image": "anyscale/ray-ml:pinned-nightly"})
    assert builder._cluster_env_name is None
    assert builder._cluster_env_dict == {"base_image": "anyscale/ray-ml:pinned-nightly"}

    with pytest.raises(RuntimeError):
        # Must provide build identifier if using compute config path and starting
        # session from sdk (with runtime env)
        builder.connect()
    builder.cluster_env(
        {"name": "test-app-config", "base_image": "anyscale/ray-ml:pinned-nightly"}
    ).connect()

    builder._start_session.assert_called_once_with(
        project_id=project_test_data.id,
        cluster_name="cluster-0",
        build_id="build_id",
        compute_template_id="mock_compute_template_id",
    )


def test_get_wheel_url() -> None:
    wheel_prefix = (
        "https://s3-us-west-2.amazonaws.com/ray-wheels/master/COMMIT_ID/ray-2.0.0.dev0"
    )
    assert (
        get_wheel_url("master/COMMIT_ID", "36", "darwin")
        == f"{wheel_prefix}-cp36-cp36m-macosx_10_13_intel.whl"
    )
    assert (
        get_wheel_url("master/COMMIT_ID", "37", "darwin")
        == f"{wheel_prefix}-cp37-cp37m-macosx_10_13_intel.whl"
    )
    assert (
        get_wheel_url("master/COMMIT_ID", "38", "darwin")
        == f"{wheel_prefix}-cp38-cp38-macosx_10_13_x86_64.whl"
    )

    assert (
        get_wheel_url("master/COMMIT_ID", "36", "linux")
        == f"{wheel_prefix}-cp36-cp36m-manylinux2014_x86_64.whl"
    )
    assert (
        get_wheel_url("master/COMMIT_ID", "37", "linux")
        == f"{wheel_prefix}-cp37-cp37m-manylinux2014_x86_64.whl"
    )
    assert (
        get_wheel_url("master/COMMIT_ID", "38", "linux")
        == f"{wheel_prefix}-cp38-cp38-manylinux2014_x86_64.whl"
    )

    assert (
        get_wheel_url("master/COMMIT_ID", "36", "win32")
        == f"{wheel_prefix}-cp36-cp36m-win_amd64.whl"
    )
    assert (
        get_wheel_url("master/COMMIT_ID", "37", "win32")
        == f"{wheel_prefix}-cp37-cp37m-win_amd64.whl"
    )
    assert (
        get_wheel_url("master/COMMIT_ID", "38", "win32")
        == f"{wheel_prefix}-cp38-cp38-win_amd64.whl"
    )


def test_commit_url_is_valid() -> None:
    for python_version in ["36", "37", "38"]:
        for pltfrm in ["win32", "linux", "darwin"]:
            url = get_wheel_url(
                "master/{}".format(REQUIRED_RAY_COMMIT), python_version, pltfrm
            )
            # We use HEAD, because it is faster than downloading with GET
            resp = requests.head(url)
            assert resp.status_code == 200, f"Cannot find wheel for: {url}"


def test_version_mismatch() -> None:
    sdk = Mock()
    _api_client = Mock()
    connect_instance = ClientBuilder(anyscale_sdk=sdk, api_client=_api_client)
    connect_instance_ignore = ClientBuilder(
        anyscale_sdk=sdk, _ignore_version_check=True, api_client=_api_client
    )

    both_wrong = ["1.1.0", "fake_commit"]
    commit_is_wrong = [REQUIRED_RAY_VERSION, REQUIRED_RAY_COMMIT[2:]]
    version_is_wrong = ["1.0.0", REQUIRED_RAY_COMMIT]
    for attempt in [both_wrong, version_is_wrong, commit_is_wrong]:
        with pytest.raises(ValueError):
            connect_instance._check_required_ray_version(*attempt)
        connect_instance_ignore._check_required_ray_version(*attempt)

    both_correct = [REQUIRED_RAY_VERSION, REQUIRED_RAY_COMMIT]
    connect_instance_ignore._check_required_ray_version(*both_correct)
    connect_instance._check_required_ray_version(*both_correct)


def test_set_metadata_in_job_config() -> None:
    sdk = Mock()
    _api_client = Mock()
    sdk.get_project.return_value = Mock(result=Mock(creator_id="mock_creator_id"))

    def mock_set_metadata(key: str, val: str) -> None:
        connect_instance._job_config.metadata[key] = val

    # Test no user specified job name
    connect_instance = ClientBuilder(anyscale_sdk=sdk, api_client=_api_client)
    connect_instance._job_config.metadata = {}
    connect_instance._job_config.set_metadata = mock_set_metadata
    connect_instance._set_metadata_in_job_config("mock_project_id")
    assert connect_instance._job_config.metadata["job_name"].startswith("job")
    assert connect_instance._job_config.metadata["creator_id"] == "mock_creator_id"

    # Test user specified job name
    connect_instance = ClientBuilder(anyscale_sdk=sdk, api_client=_api_client)
    connect_instance._job_config.metadata = {}
    connect_instance._job_config.set_metadata = mock_set_metadata
    connect_instance.job_name("mock_job_name")._set_metadata_in_job_config(
        "mock_project_id"
    )
    assert connect_instance._job_config.metadata["job_name"].startswith("mock_job_name")
    assert connect_instance._job_config.metadata["creator_id"] == "mock_creator_id"


def test_namespace() -> None:
    sdk = Mock()
    _api_client = Mock()

    # Test no user specified job name
    connect_instance = ClientBuilder(anyscale_sdk=sdk, api_client=_api_client)

    def mock_set_ray_namespace(namespace: str) -> None:
        connect_instance._job_config.ray_namespace = namespace

    connect_instance._job_config.set_ray_namespace = mock_set_ray_namespace
    connect_instance.namespace("mock_namespace")
    assert connect_instance._job_config.ray_namespace == "mock_namespace"


def test_set_runtime_env_in_job_config(
    tmp_path: Path, project_test_data: Project
) -> None:

    sdk = Mock()
    _api_client = Mock()
    connect_instance = ClientBuilder(anyscale_sdk=sdk, api_client=_api_client)
    connect_instance.env({"working_dir": "/tmp"})._set_runtime_env_in_job_config("/")
    assert connect_instance._job_config.runtime_env["working_dir"] == "/tmp"
    assert connect_instance._job_config.runtime_env["excludes"] == [
        ".git",
        "__pycache__",
        "/.anyscale.yaml",
        "/session-default.yaml",
    ]

    connect_instance = ClientBuilder(anyscale_sdk=sdk, api_client=_api_client)
    connect_instance.env({})._set_runtime_env_in_job_config("/tmp")
    assert connect_instance._job_config.runtime_env["working_dir"] == "/tmp"
    assert connect_instance._job_config.runtime_env["excludes"] == [
        ".git",
        "__pycache__",
        "/tmp/.anyscale.yaml",
        "/tmp/session-default.yaml",
    ]

    connect_instance = ClientBuilder(anyscale_sdk=sdk, api_client=_api_client)
    connect_instance.env(
        {"working_dir": "/tmp", "excludes": [".gitignore"], "pip": ["numpy"]}
    )._set_runtime_env_in_job_config("/")
    assert connect_instance._job_config.runtime_env["working_dir"] == "/tmp"
    assert connect_instance._job_config.runtime_env["excludes"] == [
        ".git",
        "__pycache__",
        "/.gitignore",
        "/.anyscale.yaml",
        "/session-default.yaml",
    ]
    assert connect_instance._job_config.runtime_env["pip"] == ["numpy"]

    connect_instance, sdk, _, _ = _make_test_builder(tmp_path, [])
    sdk.create_project.return_value = ProjectResponse(result=project_test_data)

    connect_instance.env({"working_dir": "/tmp"}).project_dir("/tmp").connect()
    connect_instance._job_config.set_runtime_env.assert_called_once_with(  # type: ignore
        {
            "working_dir": "/tmp",
            "excludes": [
                ".git",
                "__pycache__",
                "/tmp/.anyscale.yaml",
                "/tmp/session-default.yaml",
            ],
        }
    )
    connect_instance._start_session.assert_called_once_with(  # type: ignore
        project_id=ANY,
        cluster_name="cluster-0",
        build_id="build_id",
        compute_template_id="mock_compute_template_id",
    )


def test_is_in_shell() -> None:
    def frame_mock(name: str) -> Any:
        mock = Mock()
        mock.filename = name
        return mock

    anycale_call_frames = [
        "/path/anyscale/connect.py",
        "/path/anyscale/connect.py",
        "/path/anyscale/__init__.py",
    ]

    ipython_shell = [
        "<ipython-input-2-f869cc61c5de>",
        "/home/ubuntu/anaconda3/envs/anyscale/bin/ipython",
    ]
    assert _is_in_shell(list(map(frame_mock, anycale_call_frames + ipython_shell)))

    python_shell = ["<stdin>"]
    assert _is_in_shell(list(map(frame_mock, anycale_call_frames + python_shell)))

    # Running file via `ipython random_file.py`
    ipython_from_file = [
        "random_file.py",
        "/home/ubuntu/anaconda3/envs/anyscale/bin/ipython",
    ]
    assert not _is_in_shell(
        list(map(frame_mock, anycale_call_frames + ipython_from_file))
    )

    # Running file via `python random_file.py`
    python_from_file = ["random_file.py"]
    assert not _is_in_shell(
        list(map(frame_mock, anycale_call_frames + python_from_file))
    )


@pytest.mark.skip(
    "This test is very, very long, and should only be run locally if connect.py::PINNED_IMAGES are updated"
)
def test_pinned_images() -> None:
    """
    This test should be run every time PINNED_IMAGES is changed in connect.py.
    This test ensures:
    - Python versions match.
    - Ray commits match.
    - CUDA is present for GPU images (determined by the presence of the file /usr/local/cuda)
    """
    for image, pinned_image in PINNED_IMAGES.items():
        cmd = "-c \"python --version; python -c 'import ray; print(ray.__commit__)'; ls -l 2>&1 /usr/local/cuda/bin/nvcc; anyscale --version\""
        print(f"Checking: {image} with SHA: {pinned_image} ")
        output = subprocess.run(  # noqa: B1
            f"docker run --rm -it --entrypoint=/bin/bash {pinned_image} {cmd}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        py_version, ray_commit, cuda_info, anyscale_version, _ = output.stdout.decode(
            "UTF-8"
        ).split("\n")

        _, desired_py_version, desired_arch = image.split(":")[-1].split("-")
        assert (
            desired_py_version[-1] in py_version
        ), f"Wrong python version found in {pinned_image}!"

        if desired_arch == "gpu":
            assert ("ls: cannot access" not in cuda_info) and (
                "nvcc" in cuda_info
            ), f"CUDA install incorrect in {pinned_image}"
        else:
            assert (
                "ls: cannot access"
            ) in cuda_info, f"CUDA found in CPU image {pinned_image}"

        assert (
            ray_commit.strip() == REQUIRED_RAY_COMMIT
        ), f"Wrong ray commit installed in {pinned_image}"

        assert (
            anyscale_version.strip() == anyscale.__version__
        ), f"Anyscale version is different than latest master in {pinned_image}"
