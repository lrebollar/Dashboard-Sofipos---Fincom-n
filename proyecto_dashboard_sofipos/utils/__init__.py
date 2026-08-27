# Funciones de ejecución y validación 
## Fecha de actualización 28 de julio de 2026

from .f_graficos import *

# Recoge las listas __all__ de cada módulo
from .f_graficos import __all__ as _graf_all

__all__ = [*_graf_all]

# Limpia nombres internos
del _graf_all

__version__ = "1.0"
