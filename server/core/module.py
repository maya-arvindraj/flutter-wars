from fastapi import FastAPI, APIRouter
from typing import Protocol, List

class FeatureModule(Protocol):
    name: str
    router: APIRouter

class ModuleRegistry:
    def __init__(self):
        self._registered_modules: List[str] = []

    def register_module(self, app: FastAPI, module: FeatureModule) -> None:
        if module.name in self._registered_modules:
            raise RuntimeError(f"Module '{module.name}' is already registered.")
        app.include_router(module.router)
        self._registered_modules.append(module.name)

module_registry = ModuleRegistry()