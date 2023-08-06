"""
Test for the module mod:`mrtinydbutils.middelewares`.

.. moduleauthor:: Michael Rippstein <info@anatas.ch>

"""

import unittest

from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from mrtinydbutils.middlewares import DocIdToEntryMiddleware


class TestTableUuid(unittest.TestCase):
    """Tests the class `mrtinydbutils.middlewares.DocIdToEntryMiddleware`."""

    def setUp(self) -> None:
        """Test setup."""
        self.db = TinyDB(storage=DocIdToEntryMiddleware(MemoryStorage))
