import os

import pytest


@pytest.fixture(scope='function')
def env_setup(request):
    envs = request.param
    for key, value in envs.items():
        os.environ[key] = value
    yield
    for key in envs.keys():
        os.environ.pop(key, None)