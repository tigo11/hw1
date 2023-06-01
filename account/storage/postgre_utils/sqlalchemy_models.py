from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base

from account.model import AccountStatus


Base = declarative_base()


class AccountModel(Base):

    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    phone_number = Column(String, nullable=False)
    password = Column(String, nullable=False)
    status = Column(Enum(AccountStatus), nullable=False)