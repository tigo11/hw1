from typing import Optional, List
import redis

from account.model import Account, AccountStatus
from account.storage.protocol import AccountsStorageProtocol


class AccountsRedisStorage(AccountsStorageProtocol):
    def __init__(self):
        self.client = redis.Redis(host='localhost', port=6379, db=0)
        self.key_prefix = 'accounts:'

    def get_all_accounts(self) -> List[Account]:
        accounts = []
        keys = self.client.keys(f'{self.key_prefix}*')
        for key in keys:
            if b'next_id' not in key:
                account_data = self.client.get(key)
                if account_data is not None:
                    account = Account.from_json(account_data)
                    accounts.append(account)
        accounts.sort(key=lambda account: int(account.id))
        return accounts

    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        account_data = self.client.get(f'{self.key_prefix}{account_id}')
        if account_data:
            account_data_str = account_data.decode('utf-8')
            account = Account.from_json(account_data_str)
            return account
        return None

    def mark_account_as_blocked(self, account_id: int):
        account = self.get_account_by_id(account_id)
        if account is not None:
            account.status = AccountStatus.BLOCKED
            self.client.set(f'{self.key_prefix}{account_id}', account.as_json())

    def add_account(self) -> int:
        new_acc_id = self.client.incr(f'{self.key_prefix}next_id')
        new_acc = Account(
            id=new_acc_id,
            password='password',
            phone_number='88002000600',
        )
        self.client.set(f'{self.key_prefix}{new_acc_id}', new_acc.as_json())
        return new_acc_id

    def set_account_processing(self, account_id: int):
        account = self.get_account_by_id(account_id)
        if account is not None:
            account.status = AccountStatus.PROCESSING
            self.client.set(f'{self.key_prefix}{account_id}', account.as_json())

    def set_account_pending(self, account_id: int):
        account = self.get_account_by_id(account_id)
        if account is not None:
            account.status = AccountStatus.PENDING
            self.client.set(f'{self.key_prefix}{account_id}', account.as_json())

    def flush(self):
        self.client.flushdb()
