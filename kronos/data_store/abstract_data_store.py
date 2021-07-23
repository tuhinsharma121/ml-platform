from abc import abstractmethod


class AbstractDataStore(object):

    @abstractmethod
    def run_custom_update_sql(self, query):
        raise NotImplementedError("Method not implemented!")

    @abstractmethod
    def run_custom_select_sql(self, query):
        raise NotImplementedError("Method not implemented!")

    @abstractmethod
    def close_connection(self):
        raise NotImplementedError("Method not implemented!")
