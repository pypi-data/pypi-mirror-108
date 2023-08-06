mrtinydbutils - Utilities for the TinyDB
========================================

The `mrtinydbutils` provide new `Table` classes witch add the function
- to add crate and modification date
- use `uuid` as `doc_id`.

A new `Middleware` witch add the `doc_id` to the resulting `dict`.

For more information about the TinyDB see: https://github.com/msiemens/tinydb

Usage
-----

License
-------
GNU AFFERO GENERAL PUBLIC LICENSE Version 3

Developer guide
---------------

Upgrade your setup tools and pip.
They are needed for development and testing only:

.. code:: bash

    pip install --upgrade setuptools pip wheel

Development steps for code changes

.. code:: bash

    git clone https://gitlab.com/anatas_ch/pyl_mrtinydb.git
    pip install -e pyl_mrtinydb
    cd pya_bibref

Then install relevant development requirements:

.. code:: bash

    pip install -r requirements_rnd.txt
    pip install -r tests/requirements.txt

Once you have finished your changes, please provide test case(s) and relevant
documentation.
