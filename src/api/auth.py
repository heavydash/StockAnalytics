from fastapi import APIRouter
from starlette import status as http_status


from auth.schemas import RegistrationIn


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    path='/register',
    name='Create new auth',
    status_code=http_status.HTTP_201_CREATED
)
def register_in(data: RegistrationIn):
    ...



