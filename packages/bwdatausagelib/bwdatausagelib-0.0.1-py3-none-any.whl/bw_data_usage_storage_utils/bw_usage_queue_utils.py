import logging
from azure.storage.queue import QueueClient


def get_data_usage_provider_queue(data_usage_provider: str = "", connection_string: str = None):
    '''
    Get the queue client based on sim provider name given.
    If queue does not exist, a new one will be created with the
    queue storage name from sim provider name and
    transformed into lowercase as required
    '''
    try:
        queue = QueueClient.from_connection_string(
            conn_str=connection_string, queue_name=data_usage_provider.lower())
        try:
            queue.create_queue()
        except Exception as err:
            logging.error(f'create queue: {err}')
            return queue

    except Exception as err:
        logging.error(f'get queue client from {connection_string}: {err}')


def get_query_message_list(queue: QueueClient, query_set_size=int):
    '''
    Read the messages in the queue given and return the set of messages 
    as per size given. The returned message will be removed from the queue.
    '''
    queue_message_pages = list(queue.receive_messages(
        messages_per_page=query_set_size).by_page())
    queue_message_list = []

    if len(queue_message_pages) == 0:
        return [], True

    for queue_message in queue_message_pages[0]:
        queue_message_list.append(queue_message)
        queue.delete_message(queue_message)

    is_queue_size_low = False
    if len(queue_message_pages) < 1:
        is_queue_size_low = True

    return queue_message_list, is_queue_size_low
