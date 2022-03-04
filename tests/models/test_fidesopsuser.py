from sqlalchemy.orm import Session
from fidesops.models.fidesops_user import FidesopsUser


class TestFidesopsUser:
    def test_create_user(self, db: Session) -> None:
        user = FidesopsUser.create(
            db=db,
            data={"username": "user_1", "password": "test_password"},
        )

        assert user.username == "user_1"
        assert user.password == "test_password"
        assert user.created_at is not None
        assert user.updated_at is not None
