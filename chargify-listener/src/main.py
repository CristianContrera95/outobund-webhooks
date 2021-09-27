import os
import logging
import re
from base64 import b64decode

from settings import LOGGER_NAME # call to load env vars
from core.payment import save_payment
from db.hasura import GraphQL
from schema.exceptions import InvalidData


logger = logging.getLogger(LOGGER_NAME)

MONEY_CONVERTED = 100


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
    logger.info(f'/post chargify payment.\nContext:\n{context}')
    if context:
        context.callbackWaitsForEmptyEventLoop = False

    check_clients()

    try:
        body = event.get("body")
        body = b64decode(body).decode()

        webhook_id = re.search("(?<=&payload\[event_id\]=)\d+$", body).group()
        subscription_id = re.search("(?<=\[subscription\]\[id\]=)\d+(?=&)", body).group()
        amount_in_cents = re.search("(?<=\[transaction\]\[amount_in_cents\]=)\d+(?=&)", body).group()
        payment_id = re.search("(?<=\[transaction\]\[memo\]=)[\w-]+(?=%20)", body).group()

        amount = int(amount_in_cents) * MONEY_CONVERTED

        affected_rows = save_payment(subscription_id, amount, webhook_id, payment_id, graphql)
        if affected_rows:
            return {"statusCode": 200}
        else:
            return {
                "statusCode": 200,
                "body": "no changes"
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
#             "event": "payment_success",
#             "site": {"id": 77223},
#             "subscription":
#                 {"id": 46991062},
#             "transaction":
#                 {"amount_in_cents": 10050, "memo": "cf4af6ba-3fcf-4eb5-9b03-10a12980abb6"}
#         }
#     ))
