import os
import json
import logging

from db.hasura import campaign as campaign_db
from settings import LOGGER_NAME


logger = logging.getLogger(LOGGER_NAME)


def save_msg_results(wpp_id, status, graphql, lambda_client, error_msg=None):
    logger.info(f"Get from wpp {wpp_id}")

    campaign_id = None

    if status == "delivered":
        campaign_id = campaign_db.update_msg(wpp_ids=[wpp_id],
                               status=campaign_db.eventStatus.delivered,
                               error_desc='',
                               graphql=graphql)

    if  status == "read":
        campaign_id = campaign_db.update_msg(wpp_ids=[wpp_id],
                               status=campaign_db.eventStatus.read,
                               error_desc='',
                               graphql=graphql)

    if  status == "failed":
        campaign_id = campaign_db.update_msg(wpp_ids=[wpp_id],
                               status=campaign_db.eventStatus.error,
                               error_desc=error_msg if error_msg is not None else "Unknow error",
                               graphql=graphql)


    if campaign_id is not None:

        logger.info(f'Invoke lambda {os.getenv("LAMBDA_PRODUCER_NAME")}')
        response = lambda_client.invoke(FunctionName=os.getenv('LAMBDA_PRODUCER_NAME'),
                                        InvocationType='Event',
                                        Payload=json.dumps({'campaign_id': campaign_id}))

        if response['StatusCode'] == 202:
            logger.info('Invoke lambda successfully')
            return

        raise Exception
