import logging

LOG_FORMAT = "%(asctime)s:%(levelname)s:%(name)s:%(funcName)s:%(message)s"
logging.basicConfig(filename='./CHGraph.log', level=logging.WARNING, format=LOG_FORMAT)
logger = logging.getLogger('CHGraph')


class CHGraph(object):

    def __init__(self, client):
        self.client = client
        logger.info('CHGraph Start')

    def execute(self, sql):
        res = self.client.query_dataframe(sql)
        logger.info("execute sql", sql)
        return res
