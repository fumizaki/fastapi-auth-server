from typing import Optional
from src.domain.core.type.CoreValueType import RecordId
from src.domain.v1.type.AccountValueType import AccountEmail
from src.domain.v1.type.ClientValueType import ApplicationRoleType
from src.domain.v1.entity.AccountEntity import AccountEntity
from src.domain.v1.entity.ClientApplicationEntity import ClientApplicationEntity
from src.domain.v1.entity.ClientApplicationMemberEntity import ClientApplicationMemberEntity
from src.domain.v1.schema.ClientApplicationSchema import (
    InviteMemberSchema
)
from src.domain.v1.repository.AccountRepository import AccountRepository
from src.domain.v1.repository.ClientApplicationRepository import ClientApplicationRepository
from src.domain.v1.repository.ClientApplicationMemberRepository import ClientApplicationMemberRepository
from src.infrastructure.core.auth.model.OAuth2Model import Credential
from src.infrastructure.core.rdb.util.RdbSessionClient import RdbSessionClient
from src.infrastructure.core.rdb.exception.RdbException import RdbContraintError



class ClientApplicationMemberUsecase:

    class UnitOfWork:
        def __init__(
            self,
            rdb: RdbSessionClient,
            account_repository: AccountRepository,
            client_application_repository: ClientApplicationRepository,
            client_application_member_repository: ClientApplicationMemberRepository
        ) -> None:
            self.rdb = rdb
            self.account_repository = account_repository
            self.client_application_repository = client_application_repository
            self.client_application_member_repository = client_application_member_repository

    def __init__(
        self,
        credential: Credential,
        rdb: RdbSessionClient,
        account_repository: AccountRepository,
        client_application_repository: ClientApplicationRepository,
        client_application_member_repository: ClientApplicationMemberRepository
    ) -> None:
        self.credential = credential
        self.uow = self.UnitOfWork(
            rdb,
            account_repository,
            client_application_repository,
            client_application_member_repository
        )
            
            
    def v1_invite_member_exec(self, param: InviteMemberSchema) -> None:

        def _bulk_insert_client_application_member(entity_list: list[ClientApplicationMemberEntity]) -> None:
            pass

        try:
            client_application_member_in_db: Optional[ClientApplicationMemberEntity] = self.uow.client_application_member_repository.find_by_application_and_account(param.client_id, self.credential.account_id)
            if client_application_member_in_db is None:
                raise ValueError("Client application member not found")
            
            if client_application_member_in_db.role not in [ApplicationRoleType.OWNER, ApplicationRoleType.ADMIN]:
                raise
            
            exist_member: list[ClientApplicationMemberEntity] = []
            new_member: list[AccountEmail] = []
            for email in param.emails:
                account_in_db: Optional[AccountEntity] = self.uow.account_repository.find_by_email(email)
                if account_in_db:
                    exist_member.append(
                        ClientApplicationMemberEntity(
                            application_id=param.client_id,
                            account_id=account_in_db.id,
                            role=param.role
                        )
                    )

                else:
                    new_member.append(email)

            _bulk_insert_client_application_member(exist_member)
            # TODO: すでに登録されているアカウントに対して、アプリケーションにメンバ追加されたことを通知する
            # TODO: 未登録アカウントに対して、アプリケーションに招待されたことを通知する

            
        
            return
        
        finally:
            self.uow.rdb.close()