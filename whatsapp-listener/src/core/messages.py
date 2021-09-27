import logging

from db.hasura import campaign as campaign_db
from settings import LOGGER_NAME


logger = logging.getLogger(LOGGER_NAME)


def save_msg_results(wpp_id, status, graphql, error_msg=None):
    logger.info(f"Get from wpp {wpp_id}")

    if status == "delivered":
        campaign_db.update_msg(wpp_ids=[wpp_id],
                               status=campaign_db.eventStatus.delivered,
                               error_desc='',
                               graphql=graphql)

    if  status == "read":
        campaign_db.update_msg(wpp_ids=[wpp_id],
                               status=campaign_db.eventStatus.read,
                               error_desc='',
                               graphql=graphql)

    if  status == "failed":
        campaign_db.update_msg(wpp_ids=[wpp_id],
                               status=campaign_db.eventStatus.error,
                               error_desc=error_msg if error_msg is not None else "Unknow error",
                               graphql=graphql)
