import time
import slai

from slai_cli import log, constants
from slai.clients.project import get_project_client
from slai_cli.modules.docker_client import DockerClient
from slai.clients.model import get_model_client
from slai_cli.create.local_config_helper import LocalConfigHelper


def _run_inference(*, model_name, model_version_id, docker_client):
    docker_client.create_model_environment(model_name=model_name)

    exit_code = docker_client.run_trainer(
        model_name=model_name,
        model_version_id=model_version_id,
    )


def test_model(*, model_name):
    log.action(f"Testing model: {model_name}")

    project_client = get_project_client(project_name=None)
    project = project_client.get_project()
    project_name = project["name"]
    project_id = project["id"]

    docker_client = DockerClient(project_name=project_name, project_id=project_id)
    model_client = get_model_client(
        model_name=model_name, project_name=project_client.get_project_name()
    )

    local_config_helper = LocalConfigHelper()
    local_config = local_config_helper.get_local_config()

    try:
        model_version_id = local_config["models"][model_name]["model_version_id"]
    except KeyError:
        log.action("No local config set, using default model version.")
        model_version_id = model_client.model["model_version_id"]

    log.action(f"Using model version: {model_version_id}")
    if not log.warn_confirm(
        "If your training script saves a model artifact, this will be uploaded to the slai backend, continue?",  # noqa
    ):
        return

    _ = _run_trainer(
        model_name=name,
        model_version_id=model_version_id,
        docker_client=docker_client,
    )
