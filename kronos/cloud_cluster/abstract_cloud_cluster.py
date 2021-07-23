from abc import abstractmethod


class AbstractCloudCluster(object):

    @abstractmethod
    def submit_job_to_cluster(self, **kwargs):
        raise NotImplementedError("Method not implemented!")

    @abstractmethod
    def get_status_of_cluster_id(self, **kwargs):
        raise NotImplementedError("Method not implemented!")
