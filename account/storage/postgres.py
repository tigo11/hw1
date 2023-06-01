from typing import Optional, List

from account.model import Account, AccountStatus
from account.storage.protocol import AccountsStorageProtocol
from account.storage.postgre_utils.sqlalchemy_models import AccountModel
from account.storage.postgre_utils.db_manipulation import create_session, delete_db


class AccountsPostgresStorage(AccountsStorageProtocol):
    def __init__(self):
        ...

    def get_all_accounts(self) -> List[Account]:
        session = create_session()
        accounts = session.query(AccountModel).all()
        session.close()

        result = []
        for account in accounts:
            data = {
                'id': account.id,
                'password': account.password,
                'phone_number': account.phone_number,
                'status': account.status
            }
            result.append(Account.from_dict(data))
        result.sort(key=lambda account: int(account.id))
        return result
    
    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        session = create_session()
        account = session.query(AccountModel).filter_by(id=account_id).first()
        session.close()

        if account is None:
            return None

        data = {
            'id': account.id,
            'password': account.password,
            'phone_number': account.phone_number,
            'status': account.status
        }
        return Account.from_dict(data)

    def mark_account_as_blocked(self, account_id: int):
        session = create_session()
        account = session.query(AccountModel).filter_by(id=account_id).first()
        if account:
            account.status = AccountStatus.BLOCKED
            session.add(account)
            session.commit()
        session.close()

    def add_account(self) -> int:
        session = create_session()
        new_account = AccountModel(phone_number='88002000600', password='password', status=AccountStatus.PENDING)
        session.add(new_account)
        session.commit()
        new_account_id = new_account.id
        session.close()
        # assert isinstance(new_account_id, int)
        return new_account_id

    def set_account_processing(self, account_id: int):
        session = create_session()
        account = session.query(AccountModel).filter_by(id=account_id).first()
        if account:
            account.status = AccountStatus.PROCESSING
            session.add(account)
            session.commit()
        session.close()

    def set_account_pending(self, account_id: int):
        session = create_session()
        account = session.query(AccountModel).filter_by(id=account_id).first()
        if account:
            account.status = AccountStatus.PENDING
            session.add(account)
            session.commit()
        session.close()

    def flush(self):
        delete_db()
