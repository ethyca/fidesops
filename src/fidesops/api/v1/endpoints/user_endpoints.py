import logging
from fastapi import Security, Depends, APIRouter, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from fidesops.api import deps
from fidesops.api.v1 import urn_registry as urls
from fidesops.api.v1.urn_registry import V1_URL_PREFIX
from fidesops.models.fidesops_user import FidesopsUser
from fidesops.schemas.user import UserCreate, UserCreateResponse

from fidesops.util.oauth_util import verify_oauth_client
from sqlalchemy.orm import Session

from fidesops.api.v1.scope_registry import USER_CREATE, USER_DELETE

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Users"], prefix=V1_URL_PREFIX)


@router.post(
    urls.USERS,
    dependencies=[Security(verify_oauth_client, scopes=[USER_CREATE])],
    status_code=201,
    response_model=UserCreateResponse,
)
def create_user(
    *, db: Session = Depends(deps.get_db), user_data: UserCreate
) -> FidesopsUser:
    """Create a user given a username and password"""
    user = FidesopsUser.get_by(db, field="username", value=user_data.username)

    if user:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="Username already exists."
        )

    logger.info(f"Creating user: {user_data.username}.")

    user = FidesopsUser.create(db=db, data=user_data.dict())
    return user


@router.delete(
    urls.USER_DETAIL,
    dependencies=[Security(verify_oauth_client, scopes=[USER_DELETE])],
    status_code=204,
)
def delete_user(*, db: Session = Depends(deps.get_db), user_id: str) -> None:
    """Deletes the user with the given id"""

    user = FidesopsUser.get_by(db, field="id", value=user_id)

    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail=f"No user found with id {user_id}."
        )

    logger.info(f"Deleting user: {user_id}.")

    user.delete(db)
