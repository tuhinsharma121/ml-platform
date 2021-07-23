import json
import subprocess
import time

from kronos.cloud_cluster.emr_cluster import EMRCluster
from kronos.logging import pylogger
from kronos.logging.error_notifier import *

logger = pylogger.configure_logger(name="kronos_logger", log_path="/tmp/score.log")


def submit_scoring_job(client, params):
    """Submits scoring job to Spark Cluster

        Parameters
        ----------
        client : str
            the name of the client
        params_str : dict
            model params

        Returns
        -------
        job_id : str
            id of the job
        status : str
            status of the job (running/failed)
        """
    params_str = json.dumps(params, separators=(',', ':'))
    base_job_name = "forecast_engine_batch_score"
    str_cur_time = time.strftime("%Y_%m_%d_%H_%M_%S", time.gmtime())
    job_name = '{deployment_type}_{client}_{base_job_name}_{time}'.format(
        deployment_type=DEPLOYMENT_TYPE, base_job_name=base_job_name,
        time=str_cur_time, client=client)
    emr_log_path = "/tmp/score_forecast.log"

    args_list = ['bash',
                 '/home/hadoop/' + 'kronos_platform/scripts/forecast_engine/batch_score.sh',
                 '/home/hadoop/' + job_name + ".zip",
                 client,
                 params_str
                 ]

    logger.info("client : %s" % client)
    logger.info("params : %s" % params_str)
    logger.info("log_path : %s" % emr_log_path)

    command = "rm -rf /tmp/training.zip && \
                    rm -rf /tmp/training.zip && \
                    cd {path} && zip -r /tmp/training.zip ./kronos_platform ./kronos ./config.py ./config.ini && \
                    cp ./kronos_platform/scripts/forecast_engine/bootstrap.sh /tmp/bootstrap.sh".format(
        path=PROJECT_PATH)
    logger.info("command id : %s" % command)

    subprocess.check_output(command, shell=True)

    cluster_id, status = EMRCluster.submit_job_to_cluster(job_name=job_name,
                                                          bootstrap_file="/tmp/bootstrap.sh",
                                                          src_code_zip_file='/tmp/training.zip',
                                                          emr_args=args_list,
                                                          emr_log_path=emr_log_path)

    logger.info("cluster_id : %s" % cluster_id)
    logger.info("status : %s" % status)

    if status == "failed":
        raise Exception("training job {job_name} on cluster {cluster_id} has failed".format(
            job_name=job_name, cluster_id=cluster_id))

    return cluster_id, status


if __name__ == "__main__":
    submit_scoring_job(client="INTEL", params={})
