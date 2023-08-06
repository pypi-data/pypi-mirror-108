"""
Test for the module mod:`mrtinydbutils.tables`.

.. moduleauthor:: Michael Rippstein <info@anatas.ch>

"""

import unittest
from datetime import datetime
import time

from tinydb import TinyDB, where
from tinydb.storages import MemoryStorage

from mrtinydbutils.tables import TableUuid, TableTimestamp, TableUuidTimestamp


class TestTableUuid(unittest.TestCase):
    """Tests the class `mrtinydbutils.tables.TableUuid`."""

    def setUp(self) -> None:
        """Test setup."""
        TinyDB.table_class = TableUuid
        self.db = TinyDB(storage=MemoryStorage)

    def test_id_format(self) -> None:
        """Test if `id` format is a UUID verion 4 string."""
        res = self.db.insert({'test': 'test_id_format'})
        self.assertRegex(res, r'^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z')

    def test_insert_readback(self) -> None:
        """Test if `id` in the table the same."""
        self.db.truncate()  # clear db
        new_doc_id = self.db.insert({'test': 'test_insert_readback'})
        res = self.db.all()[0]
        doc_id = res.doc_id
        self.assertEqual(new_doc_id, doc_id)


class TestTableTimestamp(unittest.TestCase):
    """Tests the class `mrtinydbutils.tables.TableTimestamp`."""

    def setUp(self) -> None:
        """Test setup."""
        TinyDB.table_class = TableTimestamp
        self.db = TinyDB(storage=MemoryStorage)

    def test_insert(self) -> None:
        """Test the `insert` methode."""
        self.db.truncate()  # clear db
        new_doc_id = self.db.insert({'test': 'test_insert'})
        entry = self.db.get(doc_id=new_doc_id)
        created_at = entry[TableTimestamp.created_key]
        updated_at = entry[TableTimestamp.updated_key]
        self.assertEqual(created_at, updated_at)

    def test_insert_multiple(self) -> None:
        """Test the `insert_multiple` methode."""
        self.db.truncate()  # clear db
        self.db.insert_multiple([{'test': 'test_insert_multiple', 'count': 1},
                                 {'test': 'test_insert_multiple', 'count': 2},
                                 {'test': 'test_insert_multiple', 'count': 3}])
        created_at = []
        updated_at = []
        for n in range(3):
            entry = self.db.all()[n]
            created_at.append(entry[TableTimestamp.created_key])
            updated_at.append(entry[TableTimestamp.updated_key])
        for n in range(3):
            for i in range(3):
                self.assertEqual(created_at[n], updated_at[i])

    def test_update(self) -> None:
        """Test the `insert_multiple` methode."""
        self.db.truncate()  # clear db
        new_doc_id = self.db.insert({'test': 'test_update', 'count': 0})
        time.sleep(0.1)
        self.db.update({'count': 99})
        entry = self.db.get(doc_id=new_doc_id)
        created_at = datetime.fromisoformat(entry[TableTimestamp.created_key])
        updated_at = datetime.fromisoformat(entry[TableTimestamp.updated_key])
        self.assertGreater(updated_at, created_at)

    def test_update_multiple(self) -> None:
        """Test the `insert_multiple` methode."""
        self.db.truncate()  # clear db
        new_doc_ids = self.db.insert_multiple([{'test': 'test_update_multiple', 'count': 1},
                                               {'test': 'test_update_multiple', 'count': 2},
                                               {'test': 'test_update_multiple', 'count': 3}])
        time.sleep(0.1)
        self.db.update_multiple([({'count': 'zwei'}, where('count') == 2),
                                 ({'count': 'eins'}, where('count') == 1)])
        created_at = []
        updated_at = []
        for di in new_doc_ids:
            entry = self.db.get(doc_id=di)
            created_at.append(entry[TableTimestamp.created_key])
            updated_at.append(entry[TableTimestamp.updated_key])
        self.assertEqual(created_at[2], updated_at[2])
        self.assertGreater(updated_at[1], created_at[1])
        self.assertGreater(updated_at[0], created_at[0])
        self.assertEqual(created_at[0], created_at[2])


class TestTableUuidTimestamp(TestTableUuid, TestTableTimestamp):
    """Tests the class `mrtinydbutils.tables.TableUuidTimestamp`."""

    def setUp(self) -> None:
        """Test setup."""
        TinyDB.table_class = TableUuidTimestamp
        self.db = TinyDB(storage=MemoryStorage)


if __name__ == '__main__':
    unittest.main()
