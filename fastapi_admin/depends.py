from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from starlette.requests import Request

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_admin(request: Request, token: str = Depends(oauth2_scheme)):
    # You can replace this logic with your actual auth
    admin_user = getattr(request.state, "admin_user", None)
    if not admin_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated as admin",
        )
    return admin_user
