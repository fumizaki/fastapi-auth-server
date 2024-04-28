import uuid
from src.domain.core.entity.CoreEntity import CoreEntity
from src.domain.v1.type.AccountValueType import (
    AccountId, AccountSecretId,
    AccountPassword, AccountPasswordSalt, AccountPasswordStretching
)

class AccountSecretEntity(CoreEntity):
    id: AccountSecretId = str(uuid.uuid4())
    account_id: AccountId
    password: AccountPassword
    salt: AccountPasswordSalt
    stretching: AccountPasswordStretching