from enum import Enum
import datetime as dt

from gql.transport.exceptions import TransportQueryError

from schema.exceptions import InvalidData


class eventStatus(Enum):
    error = 'error'
    read = 'read'
    deleted = 'deleted'
    delivered = 'delivered'


def update_msg(wpp_ids, status, error_desc, graphql):
    try:
        result = graphql.query(f"""
          mutation UpdateStates {{
            update_campaign_contact(where: {{
              wpp_id: {{_in: {wpp_ids}}}
            }},
            _set: {{
              event_status_id: {status.value}
              error_description: "{error_desc}"
              last_update: "{dt.datetime.now()}"
            }})
            {{
              returning {{
                campaing_id
              }}
              affected_rows
            }}
          }}
        """.replace("'", '"'))

        return result['update_campaign_contact']['returning'][0]['campaing_id']
    except TransportQueryError as err:
        raise InvalidData(f"Invalid wpp_id: {wpp_ids}")