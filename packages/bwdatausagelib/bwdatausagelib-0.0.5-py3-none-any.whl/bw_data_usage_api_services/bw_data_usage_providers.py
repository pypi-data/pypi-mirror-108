from .bw_object_factory import ObjectFactory
from .bw_api_service_SGSingtelM2M import SGSingtelM2MServiceBuilder
from .bw_api_service_kpn import KPNServiceBuilder


class DataUsageApiServiceProvider(ObjectFactory):
    def get(self, service_id: str):
        '''
        get the API service provider for [service_id]   
        '''
        return self.create(service_id)

class DataUsageProviders():
    '''
    A Provider for all registered API services
    '''
    def __init__(self) -> None:
        self.services = DataUsageApiServiceProvider()
        self.services.register_builder('SG-Singtel-M2M', SGSingtelM2MServiceBuilder())
        self.services.register_builder('KPN', KPNServiceBuilder())
