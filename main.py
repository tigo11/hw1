from dataclasses import dataclass

from account.model import AccountStatus
from account.storage.protocol import AccountsStorageProtocol
from account.storage.postgres import AccountsPostgresStorage
from account.storage.mongo import AccountsMongoStorage
from account.storage.redis_ import AccountsRedisStorage


@dataclass
class AccountManager:
    accounts_storage: AccountsStorageProtocol

    def register_10_accounts(self):
        for _ in range(10):
            self.accounts_storage.add_account()

    def block_last_account(self):
        accounts = self.accounts_storage.get_all_accounts()
        last_account = accounts[-1]
        self.accounts_storage.mark_account_as_blocked(last_account.id)

    def work_with_2_and_4_accounts(self):
        accounts = self.accounts_storage.get_all_accounts()
        second = accounts[1]
        fourth = accounts[3]
        self.accounts_storage.set_account_processing(second.id)
        self.accounts_storage.set_account_processing(fourth.id)


def test_main():
    realisations = [AccountsPostgresStorage, AccountsMongoStorage, AccountsRedisStorage]
    for r in realisations:
        am = AccountManager(r())
        am.accounts_storage.flush()
        am.register_10_accounts()
        am.work_with_2_and_4_accounts()
        am.block_last_account()
        accounts = am.accounts_storage.get_all_accounts()
        assert len(accounts) == 10
        assert accounts[0].status == AccountStatus.PENDING
        assert accounts[1].status == AccountStatus.PROCESSING
        assert accounts[2].status == AccountStatus.PENDING
        assert accounts[3].status == AccountStatus.PROCESSING
        assert accounts[4].status == AccountStatus.PENDING
        assert accounts[5].status == AccountStatus.PENDING
        assert accounts[6].status == AccountStatus.PENDING
        assert accounts[7].status == AccountStatus.PENDING
        assert accounts[8].status == AccountStatus.PENDING
        assert accounts[9].status == AccountStatus.BLOCKED
        print(f'With realisation {r} everything is OK')


def test_serialization():
    from account.model import Account
    account = Account(id=1, phone_number="88005553535", password="12345", status=AccountStatus.PENDING)

    to_dict = account.as_dict()
    account_from_dict = Account.from_dict(to_dict)
    assert account.id == account_from_dict.id
    assert account.phone_number == account_from_dict.phone_number
    assert account.password == account_from_dict.password
    assert account.status == account_from_dict.status

    to_json = account.as_json()
    account_from_json = Account.from_json(to_json)
    assert account.id == account_from_json.id
    assert account.phone_number == account_from_json.phone_number
    assert account.password == account_from_json.password
    assert account.status == account_from_json.status
    print(f'With realisation of serialization everything is OK')


if __name__ == '__main__':
    test_serialization()
    test_main()
