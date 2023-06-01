from typing import Optional, List
from pymongo import MongoClient

from account.model import Account, AccountStatus
from account.storage.protocol import AccountsStorageProtocol


class AccountsMongoStorage(AccountsStorageProtocol):
    def __init__(self):
        self.client = MongoClient("mongodb://localhost/")
        self.db = self.client["bank"]
        self.collection = self.db["accounts"]

    def get_all_accounts(self) -> List[Account]:
        all_accounts = self.collection.find({}, {"_id": 0})
        accounts = []
        for account in all_accounts:
            new_account = Account.from_dict(account)
            accounts.append(new_account)
        return accounts
    
    def get_account_by_id(self, account_id: int) -> Optional[Account]:
        account_data = self.collection.find_one({"id": account_id}, {"_id": 0})
        if account_data:
            account = Account.from_dict(dict(account_data))
            return account
        return None

    def mark_account_as_blocked(self, account_id: int):
        self.collection.update_one({"id": account_id}, {"$set": {"status": AccountStatus.BLOCKED.value}})

    def add_account(self) -> int:
        curr_accounts_count = self.collection.count_documents({})
        new_acc_id = curr_accounts_count + 1
        new_acc = Account(
            id=new_acc_id,
            password='password',
            phone_number='88002000600',
        )
        self.collection.insert_one(new_acc.as_dict())
        return new_acc_id

    def set_account_processing(self, account_id: int):
        self.collection.update_one({"id": account_id}, {"$set": {"status": AccountStatus.PROCESSING.value}})

    def set_account_pending(self, account_id: int):
        self.collection.update_one({"id": account_id}, {"$set": {"status": AccountStatus.PENDING.value}})

    def flush(self):
        self.collection.delete_many({})
