import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.join(BASE_DIR, 'models')
modules = [mod[:-3] for mod in os.listdir(BASE_DIR) if not mod.startswith('__') and mod != 'enums']

for module in modules:
    exec('from api.models import {}'.format(module))
