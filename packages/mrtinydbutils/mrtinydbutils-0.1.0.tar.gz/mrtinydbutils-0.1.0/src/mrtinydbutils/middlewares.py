#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TinyDB Middelware Classes.

.. moduleauthor:: Michael Rippstein <michael@anatas.ch>

"""

# -----------------------------------------------------------------------------
# -- Modul importe
# - standart Module
from typing import Any, Optional

# - zusätzliche Module
from tinydb.middlewares import Middleware
# from tinydb.storages import Storage

# - eigene Module

# -----------------------------------------------------------------------------
# -- Modul Definitionen
__all__ = ('DocIdToEntryMiddleware',)


class DocIdToEntryMiddleware(Middleware):
    """Add the `doc_id` to every entry.

    It adds the `doc_id` to every entry at the reading and removing it at the writing of the the table.
    The `doc_id` is stored with the key definded in the class attribute `doc_id_key`.

    Warnings
    --------
    If the key exists in the document it will overwriten!
    """

    doc_id_key: str = '_id'
    """The name of the key."""

    # def __init__(self, storage_cls: Storage) -> None:
    #     super().__init__(storage_cls)

    def read(self) -> Optional[dict[str, dict[str, Any]]]:
        """Add the `doc_id` to every document."""
        data = self.storage.read()
        if data is None:
            return None
        for table_name in data:
            table = data[table_name]
            for doc_id in table:
                doc = table[doc_id]
                doc[self.doc_id_key] = doc_id
        return data

    def write(self, data: dict[str, dict[str, Any]]) -> None:
        """Remove the `doc_id` from every document."""
        for table_name in data:
            table = data[table_name]
            for doc_id in table:
                doc = table[doc_id]
                # Varinate 1:
                # doc.pop(self.doc_id_key, None)
                # Variante 2:
                try:
                    del doc[self.doc_id_key]
                except KeyError:
                    pass
                # Welche ist schneller?
        self.storage.write(data)
