 from abc import ABC, abstractmethod
from fastapi_admin.app import FastAPIAdmin


class Provider(ABC):
    @abstractmethod
    async def register(self, app: FastAPIAdmin):
        pass
