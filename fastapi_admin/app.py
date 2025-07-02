from typing import Dict, List, Optional, Type

import redis.asyncio as redis
from fastapi import FastAPI
from pydantic import HttpUrl
from starlette.middleware.base import BaseHTTPMiddleware
from tortoise import Model, Tortoise
from tortoise.exceptions import OperationalError

from fastapi_admin import i18n

from . import middlewares, template
from .providers import Provider
from .resources import Dropdown
from .resources import Model as ModelResource
from .resources import Resource
from .routes import router

async def _create_admin_table_if_missing(admin_model_str: str):
    """
    Checks if the admin table exists, and creates schemas if missing.
    Call only during first deploy to avoid cyclic FK headaches permanently.
    """
    admin_model = Tortoise.get_model(admin_model_str)

    try:
        count = await admin_model.all().count()
        print(f"✅ Admin table exists with {count} records.")
    except OperationalError as e:
        print("⚠️ Admin table missing, attempting to create...")
        try:
            await Tortoise.generate_schemas()
            print("✅ Admin table created successfully.")
        except Exception as ex:
            print("❌ Failed to create admin table automatically:", ex)

class FastAPIAdmin(FastAPI):
    logo_url: str
    login_logo_url: str
    admin_path: str
    resources: List[Type[Resource]] = []
    model_resources: Dict[Type[Model], Type[Resource]] = {}
    redis: redis.Redis
    language_switch: bool = True
    favicon_url: Optional[HttpUrl] = None

    async def configure(
        self,
        redis: redis.Redis,
        logo_url: str = None,
        default_locale: str = "en_US",
        language_switch: bool = True,
        admin_path: str = "/admin",
        template_folders: Optional[List[str]] = None,
        providers: Optional[List[Provider]] = None,
        favicon_url: Optional[HttpUrl] = None,
        admin_model_str: Optional[str] = None,
        create_admin_table: bool = False,   # 🩹 added flag
    ):
        self.redis = redis
        i18n.set_locale(default_locale)
        self.admin_path = admin_path
        self.language_switch = language_switch
        self.logo_url = logo_url
        self.favicon_url = favicon_url
        if template_folders:
            template.add_template_folder(*template_folders)
        await self._register_providers(providers)

        if create_admin_table and admin_model_str:
            await _create_admin_table_if_missing(admin_model_str)

    async def _register_providers(self, providers: Optional[List[Provider]] = None):
        for p in providers or []:
            await p.register(self)

    def register_resources(self, *resource: Type[Resource]):
        for r in resource:
            self.register(r)

    def _set_model_resource(self, resource: Type[Resource]):
        if issubclass(resource, ModelResource):
            self.model_resources[resource.model] = resource
        elif issubclass(resource, Dropdown):
            for r in resource.resources:
                self._set_model_resource(r)

    def register(self, resource: Type[Resource]):
        self._set_model_resource(resource)
        self.resources.append(resource)

    def get_model_resource(self, model: Type[Model]):
        r = self.model_resources.get(model)
        return r() if r else None

app = FastAPIAdmin(
    title="FastAdmin",
    description="A fast admin dashboard based on fastapi and tortoise-orm with tabler ui.",
)
app.add_middleware(BaseHTTPMiddleware, dispatch=middlewares.language_processor)
app.include_router(router)
