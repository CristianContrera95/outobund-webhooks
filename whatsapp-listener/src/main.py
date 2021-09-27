import json
import os
import logging

from settings import LOGGER_NAME # call to load env vars
from core.messages import save_msg_results
from db.hasura import GraphQL
from schema.exceptions import InvalidData


logger = logging.getLogger(LOGGER_NAME)

# instance connections to be reused by lambda
def instance_conn(only: str = ''):
    graphql = None
    try:
        if only == 'gql' or only == '':
            logger.info("Instance graphql")
            graphql = GraphQL(os.getenv("HASURA_URL"), os.getenv("HASURA_TOKEN"))

    except Exception as ex:
        logger.exception("Lambda client cannot be created")

    return graphql

def check_clients():
    global graphql
    if graphql is None:
        graphql, _ = instance_conn('gql')

graphql = instance_conn()


def handle_campaign(event, context=None):
    logger.info(f'/post whatsapp messages.\nContext:\n{context}')
    if context:
        context.callbackWaitsForEmptyEventLoop = False

    check_clients()

    body = event.get('body')
    body = json.loads(body)
    try:
        wpp_id = body.get('id')
        status = body.get('status')
        type = body.get('type')
        errors = body.get('errors')

        if wpp_id is not None and type == 'status':

            save_msg_results(wpp_id, status, graphql, errors)

        return {
            "statusCode": 200,
        }
    except InvalidData as err:
        logger.exception(f'Exception with key Error')
        return {
            "statusCode": 400,
            "body": str(err.message)
        }
    except Exception as err:
        logger.exception(f'Exception unknown')
        return {
            "statusCode": 500,
            "body": str(err)
        }


# if __name__ == "__main__":
#     print(handle_campaign(
#         {
#             "statuses":
#                 [{
#                     "id": "gBGHVJNUZAEFbwIJQJhSqWUPuhN3",
#                     "recipient_id": "16315555555",
#                     "status": "failed",
#                     "timestamp": "1518694708",
#                     "errors": [{
#                         "code": 470,
#                         "title": "Failed to send message because you are outside the support window for freeform messages to this user. Please use a valid HSM notification or reconsider."
#                     }]
#                 }]
#         }
#     ))
