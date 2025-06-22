from fastapi_admin.app import FastAPIAdmin
from typing import Callable

class UsernamePasswordProvider:
    def __init__(self, admin_model: str, verify_password: Callable, username_field: str = "username"):
        self.admin_model = admin_model
        self.verify_password = verify_password
        self.username_field = username_field

    async def register(self, app: FastAPIAdmin):
        # Placeholder logic – implement if needed
        pass