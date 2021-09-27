from uuid import UUID
from pydantic import BaseModel


TABLE_NAME = 'account'


class Account(BaseModel):
    """Databricks models"""
    id: UUID
    name: str
    balance: int
    subscription_id: str

    def format_data(self):
        pass

    def validate_fields(self):
        return True
