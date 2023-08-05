# In object_factory.py
import logging

class ObjectFactory:
    def __init__(self):
        self._builders = {}

    def register_builder(self, key:str, builder):
        '''
        key name must be alphanumeric only
        '''
        if key.isalnum == False:
            raise ValueError("key provided is not alphanumeric")
        self._builders[key] = builder

    def create(self, key, **kwargs):
        try:       
            builder = self._builders.get(key)
            if not builder:
                raise ValueError(f'{key} for builder not found in factory')
            return builder(**kwargs)
        except Exception as err:
                logging.error(err)
                raise Exception()

       
