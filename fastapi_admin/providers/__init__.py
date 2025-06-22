from abc import ABC, abstractmethod

class Provider(ABC):
    @abstractmethod
    async def register(self, app):
        from fastapi_admin.app import FastAPIAdmin  # Delayed import
        assert isinstance(app, FastAPIAdmin)
        pass
