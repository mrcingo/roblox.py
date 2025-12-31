roblox.py
======

A lightweight Python wrapper for the Roblox API focused on user data and economy.

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
    python3 setup.py install

    # Windows
    py -3 setup.py install

Quick Example
--------------

.. code:: py

    import roblox

    async with roblox.Roblox(authorization=...) as client: # Authorization is completely optional in some cases
        await client.get_user(target=...) # ID or Name

You can find more examples in the examples directory.

Links
------

- `Roblox <https://roblox.com/>`_
- `discord.py (used as a project template) <https://github.com/rapptz/discord.py>`_
