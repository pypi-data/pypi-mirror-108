import os

def get_storage_connection_string(production_storage="AzureWebJobsStorage"):
    '''
    Get the storage connection string based on environment.
    The "AzureWebJobsStorage" in local.settings.json must be set to "UseDevelopmentStorage=true"
    The Azurite emulator storage connection string is to be set in the variable "EmulatorStorage".
    '''
    connection_string = os.getenv(production_storage)
    if connection_string == "UseDevelopmentStorage=true":
        connection_string = os.getenv("EmulatorStorage")
    return connection_string
