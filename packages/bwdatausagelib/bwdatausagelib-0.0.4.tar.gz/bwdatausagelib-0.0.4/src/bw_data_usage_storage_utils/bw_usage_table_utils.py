import logging
from azure.cosmosdb.table.tableservice import TableService

GLOBAL_SIM_TABLE="GlobalSimTable"

def get_provider_sim_list(data_usage_provider: str = "", connection_string: str = None):
    '''
    Get the sim list based on provider given.
    If table does not exist, None will be returned
    '''
    try:

        table_service = TableService(connection_string=connection_string)
        sim_entities = table_service.query_entities( GLOBAL_SIM_TABLE, filter=f"PartitionKey eq '{data_usage_provider}'", num_results=1)
        sim_queries = sim_entities.items

        while sim_entities.next_marker:
          next_sim_entities =  table_service.query_entities( GLOBAL_SIM_TABLE, filter=f"PartitionKey eq '{data_usage_provider}'", marker=sim_entities.next_marker)
          sim_queries = [*sim_queries, *next_sim_entities]
          if not next_sim_entities.next_marker:
            break    

        return sim_queries

    except Exception as err:
        logging.error(f'get sim list from {connection_string}: {err}')
        return None

def store_usage_for_provider(data_usage_provider: str , connection_string: str , usage_data: Dict ) -> None:
    '''
    Store the usage data to data_usage_provider table
    The table name generated will have no dash and underscore
    '''
    try:
        usage_data.update( {'PartitionKey':data_usage_provider, 'RowKey': str(time.time())})
        table_service = TableService(connection_string=connection_string)
                
        provider_table = data_usage_provider.replace("_","").replace("-","")

        if not table_service.exists(provider_table):
            table_service.create_table(provider_table)

        table_service.insert_entity(provider_table,entity=usage_data)
 
    except:
        logging.error(f'function: store_usage_for_provider')
        pass

def store_usage_for_provider(data_usage_provider: str , connection_string: str , usage_data: Dict ) -> None:
    '''
    Store the usage data to data_usage_provider table
    The table name generated will have no dash and underscore
    '''
    try:
        usage_data.update( {'PartitionKey':data_usage_provider, 'RowKey': str(time.time())})
        table_service = TableService(connection_string=connection_string)
                
        provider_table = data_usage_provider.replace("_","").replace("-","")

        if not table_service.exists(provider_table):
            table_service.create_table(provider_table)

        table_service.insert_entity(provider_table,entity=usage_data)
 
    except:
        logging.error(f'function: store_usage_for_provider')
        pass

