"""
Test for the module mod:`mrtinydbutils`.

.. moduleauthor:: Michael Rippstein <info@anatas.ch>

"""

import unittest

from tinydb import TinyDB
from tinydb.storages import MemoryStorage

from mrtinydbutils.tables import TableUuidTimestamp
from mrtinydbutils.middlewares import DocIdToEntryMiddleware


class TestTinydbutils(unittest.TestCase):
    """Tests the integration of `TableUuidTimestamp` and `DocIdToEntryMiddleware`."""

    def setUp(self) -> None:
        """Test setup."""
        TinyDB.table_class = TableUuidTimestamp
        self.db = TinyDB(storage=DocIdToEntryMiddleware(MemoryStorage))
