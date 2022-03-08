import getpass
from typing import List

from sqlalchemy.orm import Session

from fidesops.api.v1.scope_registry import SCOPE_REGISTRY, CLIENT_CREATE
from fidesops.common_exceptions import KeyOrNameAlreadyExists
from fidesops.core.config import config
from fidesops.db.database import init_db
from fidesops.db.session import get_db_session
from fidesops.models.client import ClientDetail
from fidesops.models.fidesops_user import FidesopsUser
from fidesops.schemas.user import UserCreate

ADMIN_UI = "admin_ui"


def collect_username_and_password(db: Session) -> UserCreate:
    """Collect username and password information and validate"""
    username = input("Enter your username: ")

    password = getpass.getpass("Enter your password: ")
    verify_pass = getpass.getpass("Enter your password again: ")
    if password != verify_pass:
        raise Exception("Passwords do not match.")

    user_data = UserCreate(username=username, password=password)
    user = FidesopsUser.get_by(db, field="username", value=user_data.username)

    if user:
        raise Exception(f"User with username '{username}' already exists.")

    return user_data


def create_user_and_client(db: Session):
    """One-time script to create the first user"""
    if db.query(ClientDetail).filter_by(fides_key=ADMIN_UI).first():
        raise KeyOrNameAlreadyExists("Admin UI Client already created.")

    user_data: UserCreate = collect_username_and_password(db)

    superuser = FidesopsUser.create(db=db, data=user_data.dict())

    scopes: List[str] = SCOPE_REGISTRY
    scopes.remove(CLIENT_CREATE)

    ClientDetail.create_client_and_secret(
        db, scopes, fides_key=ADMIN_UI, username=user_data.username
    )
    print(f"Superuser '{user_data.username}' created successfully!")
    return superuser


if __name__ == "__main__":
    init_db(config.database.SQLALCHEMY_DATABASE_URI)
    session_local = get_db_session()
    create_user_and_client(session_local())
