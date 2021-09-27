from uuid import UUID
import datetime as dt

from gql.transport.exceptions import TransportQueryError

from schema.exceptions import InvalidData


def get_account_by_subscription(subscription_id: str, graphql):
    try:
        account = graphql.query(f"""
               query getAccount {{
                 account(where: {{subscription_id: {{_eq: "{subscription_id}"}}}}) {{
                   id
                   name
                   balance
                   subscription_id
                 }}
               }}
           """)
        if account['account']:
            return account['account'][0]
    except TransportQueryError as err:
        raise InvalidData(f"Invalid subscription_id: {subscription_id}")


def update_payment(account_uid: UUID, payment_id: str, webhook_id: str, amount: int, pay_event_date, graphql):
    """
    Query and return a campaign data from db
    :param raw: bool if is True returns the campaign as it comes from the db
    """
    if pay_event_date is None:
        pay_event_date = dt.datetime.now()
    try:
        update_payment = graphql.query(f"""
            mutation setPaymentStatus {{
                update_payment(where:
                {{id: {{_eq: "{payment_id}"}},
                   _and: {{status_id: {{_eq: pending}}
                  }}
                }},
                _set: {{
                    webhook_id: "{webhook_id}",
                    status_id: done,
                    pay_event_date: "{pay_event_date}"
                }}
                )
                {{
                    affected_rows
                    returning {{
                      campaign_id
                    }}
                }}
            }}
        """)
        affected_rows = update_payment['update_payment']['affected_rows']
        # TODO: if there are two pending payments with same amount?
        if affected_rows:
            campaign_id = update_payment['update_payment']['returning'][0]['campaign_id']
            affected_rows = graphql.query(f"""
            mutation setAccountCredits {{
                update_account(where:
                {{id: {{_eq: "{account_uid}"}} }},
                  _inc: {{balance: {amount} }}
                 )
                 {{
                  affected_rows
                }}
            }}
            """)
            return campaign_id, affected_rows
    except TransportQueryError as err:
        raise InvalidData(f"Invalid account payments: {account_uid}")
