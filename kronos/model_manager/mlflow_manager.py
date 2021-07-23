import time

import mlflow
from mlflow.entities.model_registry.model_version_status import ModelVersionStatus
from mlflow.tracking.client import MlflowClient

from kronos.logging import pylogger
from kronos.logging.error_notifier import *

logger = pylogger.configure_logger(name="kronos_logger", log_path="/tmp/mlflow_manager.log")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)


class MlflowManager(object):
    def __init__(self, **kwargs):
        super(MlflowManager, self).__init__(**kwargs)

    @classmethod
    def get_or_create_experiment(cls, experiment_name):
        """Get or create an experiment using mlflow

        Parameters
        ----------
        experiment_name : str
            Name of the experiment

        Returns
        -------
        experiment : Experiment
            An mlflow experiment object containing all the information about the experiment
        """
        if mlflow.get_experiment_by_name(experiment_name) is None:
            mlflow.create_experiment(experiment_name)
        experiment_id = mlflow.get_experiment_by_name(experiment_name).experiment_id
        experiment = mlflow.get_experiment(experiment_id)
        logger.info("name : {}".format(experiment.name))
        logger.info("id : {}".format(experiment.experiment_id))
        logger.info("artifact location: {}".format(experiment.artifact_location))
        logger.info("tags : {}".format(experiment.tags))
        logger.info("lifecycle stage : {}".format(experiment.lifecycle_stage))
        return experiment

    @classmethod
    def save_python_model(cls, experiment_id, run_name=None, params=None, metrics=None, model=None):
        """Saves python model as part of the experiment using mlflow

        Parameters
        ----------
        experiment_id : str
            mlflow experiment id
        run_name : str
            Name of the mlflow run as part of the experiment.
        params : dict
            params to be stored as part of the mlflow model
        metrics : dict
            metrics to be stored as part of the mlflow model
        model : mlflow.pyfunc.PythonModel
            model object to be stored

        Returns
        -------
        run_id : str
            mlflow run id associated with the model persistance
        """
        with mlflow.start_run(run_name=run_name, experiment_id=experiment_id):
            run_id = mlflow.active_run().info.run_id
            if params is not None:
                mlflow.log_params(params)
            if metrics is not None:
                mlflow.log_metrics(metrics)
            if model is not None:
                mlflow.pyfunc.log_model("model", python_model=model)
        return run_id

    @classmethod
    def wait_until_ready(cls, model_name, model_version):
        """Holds the system execution till the model is ready

        Parameters
        ----------
        model_name : str
            name of the mlflow model
        model_version : str
            version of the mlflow model

        Returns
        -------
        None
            Waits indefinitely till the model is ready

        """
        client = MlflowClient()
        for _ in range(10):
            model_version_details = client.get_model_version(
                name=model_name,
                version=model_version,
            )
            status = ModelVersionStatus.from_string(model_version_details.status)
            logger.info("Model status: %s" % ModelVersionStatus.to_string(status))
            if status == ModelVersionStatus.READY:
                break
            time.sleep(1)

    @classmethod
    def register_model(cls, artifact_location, run_id, model_name):
        """Registers the mlflow model

        Parameters
        ----------
        artifact_location : str
            Artifact location of the mlflow experiment
        run_id : str
            Run id of the experiment
        model_name : str
            Name of the mlflow model

        Returns
        -------
        model_details : mlflow.entities.model_registry.ModelVersion
            Object created by mlflow
        """
        model_uri = "{artifact_location}/{run_id}/artifacts/model".format(
            artifact_location=artifact_location,
            run_id=run_id)
        model_details = mlflow.register_model(model_uri=model_uri, name=model_name)
        logger.info(model_uri)
        return model_details

    @classmethod
    def get_latest_model_by_stage(cls, model_name, stage):
        """Get the latest mlflow model by name and stage

        Parameters
        ----------
        model_name : str
            Name of the mlflow model
        stage : str
            Name of the stage - (None/Staging/Production/Archived)

        Returns
        -------
        model : mlflow.pyfunc.PythonModel
            The mlflow model object
        """
        client = MlflowClient()
        model_versions = client.search_model_versions("name = '%s'" % model_name)
        version_ids = list()
        for res in model_versions:
            version = int(res.version)
            current_stage = res.current_stage
            if current_stage == stage:
                version_ids.append(version)

        version_id = max(version_ids)
        model_uri = "models:/{model_name}/{version_id}".format(model_name=model_name, version_id=version_id)
        logger.info(model_uri)
        model = mlflow.pyfunc.load_model(model_uri)
        return model, model_uri
