roblox.py
======

.. image:: https://img.shields.io/pypi/v/roblox.py.svg
   :target: https://pypi.python.org/pypi/discord.py
   :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/roblox.py.svg
   :target: https://pypi.python.org/pypi/discord.py
   :alt: PyPI supported Python versions

A lightweight Python wrapper for the Roblox API focused on user data and gamepass inventory management.

Key Features
-------------

- Modern Pythonic API using ``async`` and ``await``.
- Purchase and revoke gamepasses.
- Retrieve Roblox user data (with limitations).

Installing
----------

**Python 3.8 or higher is required**

To install the library, you can just run the following command:

.. note::

    A `Virtual Environment <https://docs.python.org/3/library/venv.html>`__ is recommended to install
    the library, especially on Linux where the system Python is externally managed and restricts which
    packages you can install on it.

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U roblox.py

    # Windows
    py -3 -m pip install -U roblox.py

Quick Example
--------------

.. code:: py

    import roblox

    async with roblox.Roblox(authorization=...) as roblox: # Authorization is completely optional in some cases
        await roblox.get_user(target=...) # ID or Name

Links
------

- `Roblox <https://roblox.com/>`_
- `discord.py (used as a project template) <https://github.com/rapptz/discord.py>`_
