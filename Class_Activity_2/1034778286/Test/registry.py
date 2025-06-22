"""
Registro central de tests.  
Añade aquí cualquier nuevo caso (incluidos los que deban fallar).
"""
from Test.BackEnd_Test import integration_test as backend_ok
from Test.FrontEnd_Test import main as frontend_ok
from Test.InvalidUser_Test import run as invalid_user_fail   # <- Falla

TESTS = [
    ("Backend – OK", backend_ok),
    ("Frontend – OK", frontend_ok),
    ("Backend – Usuario inválido", invalid_user_fail),
]
