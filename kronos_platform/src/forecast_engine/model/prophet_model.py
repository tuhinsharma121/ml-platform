import mlflow
import numpy as np
from prophet import Prophet
from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics

from kronos.logging import pylogger
from kronos.logging.output_supressor import suppress_stdout_stderr
from kronos.model_manager.mlflow_manager import MlflowManager

logger = pylogger.configure_logger(name="kronos_logger", log_path="/tmp/prophet.log")

np.random.seed(40)
class_name = "prophet"


class ProphetModel(mlflow.pyfunc.PythonModel):

    def __init__(self, model):
        self.model = model
        super().__init__()

    def load_context(self, context):
        return

    def predict(self, context, model_input):
        """Overrides the method of the base class for model prediction using mlflow

        Parameters
        ----------
        context : mlflow context
        model_input : input to the model

        Returns
        -------
        the prediction of the model
        """
        return self.model.predict(model_input)

    @classmethod
    def load(cls, experiment_name, stage):
        """Load the model using mlflow

        Parameters
        ----------
        experiment_name : str
            name of the mlflow experiment
        stage : str
            Name of the stage - (None/Staging/Production/Archived)

        Returns
        -------
        model : ProphetModel
            model object
        model_name : str
            model name in the mlflow
        version :
            model version in the mlflow
        """
        model_name = "{experiment_name}-{name}".format(experiment_name=experiment_name, name=class_name)
        model, version = MlflowManager.get_latest_model_by_stage(model_name=model_name, stage=stage)
        return model, model_name, version

    @classmethod
    def train(cls, df, model_params=None):
        """Train the ProphetModel

        Parameters
        ----------
        df : pandas.Dataframe
            dataframe must contain 2 mandatory columns ds,y
        model_params : dict
            the model parameters

        Returns
        -------
        model : ProphetModel
            model object
        params : dict
            model parameters
        metrics : dict
            performance metrics of the model after doing cross validation
        """
        if model_params is None:
            model_params = {}
        hyper_params = {"rolling_window": 0.1}

        m = Prophet(**model_params)
        with suppress_stdout_stderr():
            m.fit(df)
            df_cv = cross_validation(m, initial='730 days', period='90 days', horizon='120 days', disable_tqdm=True)
            df_p = performance_metrics(df_cv, **hyper_params)

        params = {**model_params, **hyper_params}

        metrics = {"mse": df_p['mse'].mean(),
                   "rmse": df_p['rmse'].mean(),
                   "mae": df_p['mae'].mean(),
                   "mape": df_p['mape'].mean(),
                   "mdape": df_p['mdape'].mean(),
                   "smape": df_p['smape'].mean(),
                   "coverage": df_p['coverage'].mean()}

        model = ProphetModel(m)
        return model, params, metrics

    def save(self, params, metrics, experiment_name):
        """Save the model using mlflow

        Parameters
        ----------
        params : dict
            model parameters
        metrics : dict
            performance metrics of the model after doing cross validation
        experiment_name : str
            name of the mlflow experiment

        Returns
        -------
        None
        """
        experiment = MlflowManager.get_or_create_experiment(experiment_name=experiment_name)
        run_id = MlflowManager.save_python_model(experiment_id=experiment.experiment_id, run_name=class_name,
                                                 metrics=metrics, params=params, model=self)
        model_name = "{experiment_name}-{name}".format(experiment_name=experiment.name, name=class_name)
        model = MlflowManager.register_model(artifact_location=experiment.artifact_location, run_id=run_id,
                                             model_name=model_name)
        MlflowManager.wait_until_ready(model_name=model.name, model_version=model.version)
