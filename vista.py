import requests
import urllib3
from ruxit.api.base_plugin import RemoteBasePlugin
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class VistaPlugin(RemoteBasePlugin):

    
    def initialize(self, **kwargs):
        #logger.info("Config: %s", self.config)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        config = kwargs['config']
        self.url = config["url"]
        
        self.refreshCounter = 0
        self.logger.info("Initializing")
     

    def query(self, **kwargs):
        res= requests.get(self.url)
        logger.info(res.text)
        soup = BeautifulSoup(res.text, "html.parser")
        group = self.topology_builder.create_group("License Usage", "License Usage")
        table = soup.find_all('table', attrs={"class": "tpTable"})
        for eTable in table:
            table_rows = eTable.find_all('tr', attrs={"class": "tpOdd"})
            for tr in table_rows:
                logger.info("Odd rows")
                logger.info(tr)
                td = tr.find_all('td')
                value = []
                key=''
                for eTd in td:
                    j=0
                    t = eTd.get('title')
                    logger.info(t)
                    if ( t is not None):
                        if(t.isnumeric()):
                            value.append(t)
                            j=j+1
                        else:
                            key = t
                logger.info("key=%s value=%s", key, value)
                device = group.create_device(key, key)
                device.absolute(key='Local', value=value[0])
                device.absolute(key='Distributed', value=value[1])
            table_rows = eTable.find_all('tr', attrs={"class": "tpEven"})
            for tr in table_rows:
                logger.info("Even rows")
                logger.info(tr)
                td = tr.find_all('td')
                value = []
                key=''
                for eTd in td:
                    j=0
                    t = eTd.get('title')
                    logger.info(t)
                    if ( t is not None):
                        if(t.isnumeric()):
                            value.append(t)
                            j=j+1
                        else:
                            key = t
                logger.info("key=%s value=%s", key, value)
                device = group.create_device(key, key)
                device.absolute(key='Local', value=value[0])
                device.absolute(key='Distributed', value=value[1])
 