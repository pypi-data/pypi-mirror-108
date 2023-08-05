import requests
from .bw_api_secrets import ApiSecrets

class SGSingtelM2MService:
    base_url = 'https://restapi1.jasper.com/rws/api/v1/devices'

    def __init__(self):
        self._api_secrets = ApiSecrets('SG-Singtel-M2M')

    def request_usage(self, iccid):
        try:
            response = requests.get(self.base_url + '/'+iccid+'/ctdUsages', auth=(self._api_secrets.user, self._api_secrets.key))
            response.raise_for_status()
            return response.json()
        except Exception :
            raise


class SGSingtelM2MServiceBuilder():
    def __init__(self):
        self._instance = None

    def __call__(self, **_ignored):
        if not self._instance:
            self._instance = SGSingtelM2MService()
        return self._instance


