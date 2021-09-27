import logging
import os

import requests

from db.hasura import account as account_db
from schema.account import Account
from settings import LOGGER_NAME


logger = logging.getLogger(LOGGER_NAME)


def save_payment(subscription_id, amount, webhook_id, payment_id, graphql):
    logger.info(f"Get from hasura subscription: {subscription_id}")
    account_data = account_db.get_account_by_subscription(subscription_id, graphql)
    if account_data is not None:
        logger.info(f"Map account data to schema")
        account_data = Account(**account_data)

        logger.info(f"Validate campaign fields")
        account_data.validate_fields()

        campaign_id, affected_rows = account_db.update_payment(account_data.id,
                                                  payment_id,
                                                  webhook_id,
                                                  amount,
                                                  None,
                                                  graphql=graphql)

        if affected_rows:
            response = requests.post(os.getenv("LAUNCH_CAMPAIGN_URL"),
                                     headers={"Authorization": os.getenv("LAUNCH_CAMPAIGN_TOKEN")},
                                     json={'campaign_id': campaign_id})
            response.raise_for_status()
        return affected_rows