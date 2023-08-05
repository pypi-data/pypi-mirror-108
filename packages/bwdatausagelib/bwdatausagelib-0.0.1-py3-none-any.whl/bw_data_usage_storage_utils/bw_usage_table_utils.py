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

