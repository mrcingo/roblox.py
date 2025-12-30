import re

from setuptools import setup


def get_init_version() -> str:
    version = ''
    with open('roblox/__init__.py') as f:
        version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE)

    if not version:
        raise RuntimeError('Version is not set')

    return version.group(1)


setup(version=get_init_version())
