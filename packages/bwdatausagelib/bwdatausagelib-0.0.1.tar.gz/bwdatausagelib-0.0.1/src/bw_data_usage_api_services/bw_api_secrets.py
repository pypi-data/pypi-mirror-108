import logging
import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential


class ApiSecrets:

    def __init__(self, service_id: str):
        '''
        Retrieves from Azure Key Vault {service_id}-api-key, {service_id}-api-user', {service_id}-api-user' \n
        Requires App Setting, `AZURE_CLIENT_ID`, `AZURE_TENANT_ID`, `AZURE_CLIENT_SECRET`, KEY_VAULT_NAME \n
        Use the Azure CLI to set store the secrets into the Azure Key Vault \n
        '''
        self.key = self._get(f'{service_id}-api-key')
        self.user = self._get(f'{service_id}-api-user')
        self.pwd = self._get(f'{service_id}-api-pwd')

    def _get(self, secret_name):
        try:
            keyVaultName = os.environ["AZURE_KEYVAULT"]
            KVUri = f"https://{keyVaultName}.vault.azure.net"
            credential = DefaultAzureCredential() 
            client = SecretClient(vault_url=KVUri, credential=credential)
            return client.get_secret(secret_name).value

        except Exception as err:
            logging.warn(f'{secret_name} unretrievable from Keyvault - {err.reason}')
            return ''
