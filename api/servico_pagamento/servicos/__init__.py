import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.join(BASE_DIR, 'servicos')
modules = [mod[:-3] for mod in os.listdir(BASE_DIR) if not mod.startswith('__') ]

for module in modules:
    command = 'from api.servico_pagamento.servicos import {}'.format(module)
    exec(command)
