import boto3

from config import *
from kronos.cloud_cluster.abstract_cloud_cluster import AbstractCloudCluster
from kronos.logging import pylogger

logger = pylogger.configure_logger(name="kronos_logger", log_path="/tmp/cloud_cluster.log")


class EMRCluster(AbstractCloudCluster):

    def __init__(self):
        super(EMRCluster).__init__()

    @classmethod
    def submit_job_to_cluster(cls, job_name, bootstrap_file, src_code_zip_file, emr_args, emr_log_path):
        """Spawns and submits python job to AWS EMR cluster

        Parameters
        ----------
        job_name : str
            Name of the EMR job to be created
        bootstrap_file : str
            Path to the bootstrap file
        src_code_zip_file : str
            Path to the source code in zip format
        emr_args : List
            The command that needs to be run in AWS EMR
        emr_log_path : str
            Path where the logs for the job needs to be stored in AWS EMR cluster

        Returns
        -------
        cluster_id : str
            Cluster id of the AWS EMR job created
        status : str
            status of the job (running/failed)
        """

        # S3 bucket/key, where the input spark job ( mlflows3 code ) will be uploaded
        s3_bucket = EMR_S3_BUCKET
        s3_code_base_name = '{job_name}.zip'.format(job_name=job_name)
        s3_code_base_uri = 's3://{bucket}/{key}'.format(bucket=s3_bucket, key=s3_code_base_name)
        s3_bootstrap_name = '{job_name}_bootstrap_action.sh'.format(job_name=job_name)
        s3_bootstrap_uri = 's3://{bucket}/{key}'.format(bucket=s3_bucket, key=s3_bootstrap_name)

        # S3 bucket/key, where the spark job logs will be maintained
        # Note: these logs are AWS logs that tell us about application-id of YARN application
        #       we need to log into EMR cluster nodes and use application-id to view YARN logs

        s3_log_bucket = EMR_S3_BUCKET
        s3_log_name = job_name + ".log"
        s3_log_uri = 's3://{bucket}/{key}'.format(bucket=s3_log_bucket, key=s3_log_name)
        logger.info("uploading the bootstrap action to AWS S3 URI %s" % s3_bootstrap_uri)
        # Note: This overwrites if file already exists
        s3_client = boto3.client('s3',
                                 aws_access_key_id=AWS_ACCESS_KEY_ID,
                                 aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                 region_name=AWS_REGION,
                                 aws_session_token=AWS_SESSION_TOKEN)

        s3_client.upload_file(bootstrap_file, s3_bucket, s3_bootstrap_name)

        logger.info("uploading the codebase to AWS S3 URI %s" % s3_code_base_uri)
        s3_client.upload_file(src_code_zip_file, s3_bucket, s3_code_base_name)

        logger.info("starting spark emr cluster and submitting the jobs")
        emr_client = boto3.client('emr',
                                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                  region_name=AWS_REGION,
                                  aws_session_token=AWS_SESSION_TOKEN)

        response = emr_client.run_job_flow(
            Name=job_name,
            LogUri=s3_log_uri,
            ReleaseLabel='emr-6.2.0',
            Instances={
                'KeepJobFlowAliveWhenNoSteps': False,
                'TerminationProtected': False,
                'Ec2SubnetId': EC2_SUBNET_ID,
                'Ec2KeyName': EC2_KEY_NAME,
                'EmrManagedMasterSecurityGroup': EC2_MASTER_SECURITY_GROUP,
                'EmrManagedSlaveSecurityGroup': EC2_SLAVE_SECURITY_GROUP,
                'InstanceGroups': [
                    {
                        'Name': '{}_master_group'.format(job_name),
                        'InstanceRole': 'MASTER',
                        'InstanceType': EC2_INSTANCE_TYPE,
                        'InstanceCount': 1,
                        'Configurations': [
                            {
                                "Classification": "spark-env",
                                "Configurations": [
                                    {
                                        "Classification": "export",
                                        "Properties": {
                                            "LC_ALL": "en_US.UTF-8",
                                            "LANG": "en_US.UTF-8",
                                            "PYTHONPATH": "/home/hadoop/",
                                            "PYSPARK_PYTHON": "/usr/bin/python3",
                                            "PYSPARK_DRIVER_PYTHON": "/usr/bin/python3",
                                            "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
                                            "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
                                            "AWS_SESSION_TOKEN": AWS_SESSION_TOKEN
                                        }
                                    }
                                ]
                            },
                            {
                                "Classification": "yarn-env",
                                "Properties": {},
                                "Configurations": [
                                    {
                                        "Classification": "export",
                                        "Configurations": [],
                                        "Properties": {
                                            "LC_ALL": "en_US.UTF-8",
                                            "LANG": "en_US.UTF-8",
                                            "PYTHONPATH": "/home/hadoop/",
                                            "PYSPARK_PYTHON": "/usr/bin/python3",
                                            "PYSPARK_DRIVER_PYTHON": "/usr/bin/python3",
                                            "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
                                            "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
                                            "AWS_SESSION_TOKEN": AWS_SESSION_TOKEN
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    # {
                    #     'Name': '{}_core_group'.format(job_name),
                    #     'InstanceRole': 'CORE',
                    #     'InstanceType': EC2_INSTANCE_TYPE,
                    #     'InstanceCount': 0,
                    #     'Configurations': [
                    #         {
                    #             "Classification": "spark-env",
                    #             "Configurations": [
                    #                 {
                    #                     "Classification": "export",
                    #                     "Properties": {
                    #                         "LC_ALL": "en_US.UTF-8",
                    #                         "LANG": "en_US.UTF-8",
                    #                         "AWS_S3_ACCESS_KEY_ID": AWS_S3_ACCESS_KEY_ID,
                    #                         "AWS_S3_SECRET_ACCESS_KEY": AWS_S3_SECRET_ACCESS_KEY,
                    #                         "PYTHONPATH": "/home/hadoop/",
                    #                         "PYSPARK_PYTHON": "/usr/bin/python3",
                    #                         "PYSPARK_DRIVER_PYTHON": "/usr/bin/python3"
                    #                     }
                    #                 }
                    #             ]
                    #         },
                    #         {
                    #             "Classification": "yarn-env",
                    #             "Properties": {},
                    #             "Configurations": [
                    #                 {
                    #                     "Classification": "export",
                    #                     "Configurations": [],
                    #                     "Properties": {
                    #                         "LC_ALL": "en_US.UTF-8",
                    #                         "LANG": "en_US.UTF-8",
                    #                         "AWS_S3_ACCESS_KEY_ID": AWS_S3_ACCESS_KEY_ID,
                    #                         "AWS_S3_SECRET_ACCESS_KEY": AWS_S3_SECRET_ACCESS_KEY,
                    #                         "PYTHONPATH": "/home/hadoop/",
                    #                         "PYSPARK_PYTHON": "/usr/bin/python3",
                    #                         "PYSPARK_DRIVER_PYTHON": "/usr/bin/python3"
                    #                     }
                    #                 }
                    #             ]
                    #         }
                    #     ]
                    # },
                    # {
                    #     'Name': '{}_task_group'.format(job_name),
                    #     'InstanceRole': 'TASK',
                    #     'InstanceType': EC2_INSTANCE_TYPE,
                    #     'InstanceCount': 0,
                    #     'Configurations': [
                    #         {
                    #             "Classification": "spark-env",
                    #             "Configurations": [
                    #                 {
                    #                     "Classification": "export",
                    #                     "Properties": {
                    #                         "LC_ALL": "en_US.UTF-8",
                    #                         "LANG": "en_US.UTF-8",
                    #                         "AWS_S3_ACCESS_KEY_ID": AWS_S3_ACCESS_KEY_ID,
                    #                         "AWS_S3_SECRET_ACCESS_KEY": AWS_S3_SECRET_ACCESS_KEY,
                    #                         "PYTHONPATH": "/home/hadoop/",
                    #                         "PYSPARK_PYTHON": "/usr/bin/python3",
                    #                         "PYSPARK_DRIVER_PYTHON": "/usr/bin/python3"
                    #                     }
                    #                 }
                    #             ]
                    #         },
                    #         {
                    #             "Classification": "yarn-env",
                    #             "Properties": {},
                    #             "Configurations": [
                    #                 {
                    #                     "Classification": "export",
                    #                     "Configurations": [],
                    #                     "Properties": {
                    #                         "LC_ALL": "en_US.UTF-8",
                    #                         "LANG": "en_US.UTF-8",
                    #                         "AWS_S3_ACCESS_KEY_ID": AWS_S3_ACCESS_KEY_ID,
                    #                         "AWS_S3_SECRET_ACCESS_KEY": AWS_S3_SECRET_ACCESS_KEY,
                    #                         "PYTHONPATH": "/home/hadoop/",
                    #                         "PYSPARK_PYTHON": "/usr/bin/python3",
                    #                         "PYSPARK_DRIVER_PYTHON": "/usr/bin/python3"
                    #                     }
                    #                 }
                    #             ]
                    #         }
                    #     ]
                    # }
                ],
            },
            Applications=[
                {
                    'Name': 'Spark'
                }
            ],
            BootstrapActions=[
                {
                    'Name': 'install dependencies',
                    'ScriptBootstrapAction': {
                        'Path': s3_bootstrap_uri
                    }
                }
            ],
            Steps=[
                {
                    'Name': 'setup debugging',
                    'ActionOnFailure': 'TERMINATE_CLUSTER',
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': ['state-pusher-script']
                    }
                },
                {
                    'Name': 'setup - copy files',
                    'ActionOnFailure': 'CANCEL_AND_WAIT',
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': ['aws', 's3', 'cp', s3_code_base_uri,
                                 '/home/hadoop/']
                    }
                },
                {
                    'Name': 'setup - unzip files',
                    'ActionOnFailure': 'CANCEL_AND_WAIT',
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': ['unzip', '/home/hadoop/' + s3_code_base_name,
                                 '-d', '/home/hadoop/']
                    }
                },
                {
                    'Name': 'run python job',
                    'ActionOnFailure': 'CONTINUE',
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': emr_args
                    }
                },
                {
                    'Name': 'save log to s3',
                    'ActionOnFailure': 'CANCEL_AND_WAIT',
                    'HadoopJarStep': {
                        'Jar': 'command-runner.jar',
                        'Args': ['aws',
                                 's3',
                                 'cp',
                                 emr_log_path,
                                 s3_log_uri]
                    }
                }
            ],
            VisibleToAllUsers=True,
            JobFlowRole='EMR_EC2_DefaultRole',
            ServiceRole='EMR_DefaultRole'
        )

        status = "failed"
        cluster_id = None
        if response.get('ResponseMetadata').get('HTTPStatusCode') == 200:
            cluster_id = response.get('JobFlowId')
            status = "running"

        return cluster_id, status

    @classmethod
    def get_status_of_cluster_id(cls, cluster_id):
        """Returns the status of AWS EMR cluster id

        Parameters
        ----------
        cluster_id : str
            AWS EMR cluster id

        Returns
        -------
        status : str
            Status of the AWS EMR cluster (running/success/failed)
        """
        status = "running"
        emr_client = boto3.client('emr',
                                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                  region_name=AWS_REGION,
                                  aws_session_token=AWS_SESSION_TOKEN)

        response = emr_client.describe_cluster(

            ClusterId=cluster_id
        )

        state = response["Cluster"]["Status"]["State"]
        state_change_reason = response["Cluster"]["Status"]["StateChangeReason"]
        if state == "TERMINATED" or state == "TERMINATED_WITH_ERRORS":
            if "Code" in state_change_reason and state_change_reason["Code"] == "ALL_STEPS_COMPLETED":
                status = "success"
                logger.info("Training job %s is completed!!" % (cluster_id))
            else:
                status = "failed"
                logger.info("Training job %s is running!!" % (cluster_id))

        return status
