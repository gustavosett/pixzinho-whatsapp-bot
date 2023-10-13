"""
Esse código adiciona todos routers para dentro de uma lista para que possa
ser utilizado no main.py
"""
import importlib
import pkgutil
from fastapi import APIRouter
from app.services.utils import LOGGER

try:
    # Obter a lista de todos os módulos no diretório atual
    modules = [name for _, name, _ in pkgutil.iter_modules([__path__[0]])]

    routers = []

    # Iterar através de todos os módulos
    for module in modules:
        # Importar o módulo
        imported_module = importlib.import_module('.' + module, package=__name__)

        # Verificar se o módulo tem uma variável chamada 'router'
        if hasattr(imported_module, 'router') and isinstance(imported_module.router, APIRouter):
            routers.append(imported_module.router)
except Exception as e:
    LOGGER.error(f"Failed to import routers, error: {e}")
