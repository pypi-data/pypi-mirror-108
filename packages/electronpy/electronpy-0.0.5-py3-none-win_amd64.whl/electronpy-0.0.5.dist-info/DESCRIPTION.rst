electronpy
==========

Introduce
---------

This is a wrapper for electron.

now using electron v9.4.1


Install
--------


Install from pypi:

.. code-block:: bash

    python -m pip install electronpy



Build wheel
-----------

Build all platfroms. Strongly suggest to build in Linux instead of win 10.

.. code-block:: bash

    python3 build.py


build wheel manually. first put the electron in directory electronpy/electron. Then

.. code-block:: bash

    python setup.py bidst_wheel --plat_name win_amd64
    python setup.py bidst_wheel --plat_name manylinux1_x86_64
    python setup.py bidst_wheel --plat_name manylinux2014_aarch64


Notice
------

The the manylinux1_x86_64 and manylinux2014_aarch64 must be build under linux environment.

When build linux platfrom whl on win32, the executable file **electron** have no executable permission

