#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
It implements additional tables for TinyDB.

.. moduleauthor:: Michael Rippstein <michael@anatas.ch>

"""

# -----------------------------------------------------------------------------
# -- Modul importe
# - standart Module
import uuid
from typing import Optional, Mapping, Iterable, List, Union, Callable, cast, Tuple, MutableMapping
from datetime import datetime, timezone

# - zusätzliche Module
from tinydb.table import Table, Document
from tinydb.storages import Storage
from tinydb.queries import Query

# - eigene Module

# -----------------------------------------------------------------------------
__all__ = ('TableUuid', 'TableTimestamp', 'TableUuidTimestamp')


class TableUuid(Table):
    """Table with uuid ids.

    Beschreibung
    """

    def __init__(
            self,
            storage: Storage,
            name: str,
            cache_size: int = Table.default_query_cache_capacity
    ) -> None:
        Table.document_id_class = str                                          # type: ignore[assignment]
        super().__init__(storage, name, cache_size)

    def _get_next_id(self) -> str:
        """Return the ID for a newly inserted document.

        Returns
        -------
        str
        """
        return str(uuid.uuid4())


class TableTimestamp(Table):
    """Table with timestamps in every entry."""

    created_key: str = '_created'
    """."""

    updated_key: str = '_updated'
    """."""

    def insert(self, document: MutableMapping) -> int:    # type: ignore[override]
        """Insert a new document into the table.

        Parameters
        ----------
        document
            the document to insert

        Returns
        -------
        int
            the inserted document's ID
        """
        # Make sure the document implements the ``Mapping`` interface
        if not isinstance(document, Mapping):
            raise ValueError('Document is not a Mapping')

        # First, we get the document ID for the new document
        if isinstance(document, Document):
            # For a `Document` object we use the specified ID
            doc_id = document.doc_id

            # We also reset the stored next ID so the next insert won't
            # re-use document IDs by accident when storing an old value
            self._next_id = None
        else:
            # In all other cases we use the next free ID
            doc_id = self._get_next_id()

        timestamp = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()
        document[self.created_key] = timestamp
        document[self.updated_key] = timestamp

        # Now, we update the table and add the document
        def updater(table: dict) -> None:
            assert doc_id not in table, 'doc_id ' + str(doc_id) + ' already exists'

            # By calling ``dict(document)`` we convert the data we got to a ``dict`` instance even if it was a
            # different class that implemented the ``Mapping`` interface
            table[doc_id] = dict(document)

        # See below for details on ``Table._update``
        self._update_table(updater)

        return doc_id

    def insert_multiple(self, documents: Iterable[MutableMapping]) -> List[int]:    # type: ignore[override]
        """Insert multiple documents into the table.

        Parameters
        ----------
        documents
            a Iterable of documents to insert

        Returns
        -------
        List[int]
            a list containing the inserted documents' IDs
        """
        doc_ids = []

        timestamp = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()

        def updater(table: dict) -> None:
            for document in documents:
                # Make sure the document implements the ``Mapping`` interface
                if not isinstance(document, Mapping):
                    raise ValueError('Document is not a Mapping')

                # Get the document ID for this document and store it so we can return all document IDs later
                doc_id = self._get_next_id()
                doc_ids.append(doc_id)

                document[self.created_key] = timestamp
                document[self.updated_key] = timestamp

                # Convert the document to a ``dict`` (see Table.insert) and store it
                table[doc_id] = dict(document)

        # See below for details on ``Table._update``
        self._update_table(updater)

        return doc_ids

    def update(                                                                 # noqa: C901
        self,
        fields: Union[Mapping, Callable[[Mapping], None]],
        cond: Optional[Query] = None,
        doc_ids: Optional[Iterable[int]] = None,
    ) -> List[int]:
        """Update all matching documents to have a given set of fields.

        Parameters
        ----------
        fields
            the fields that the matching documents will have or a method that will update the documents
        cond
            which documents to update
        doc_ids
            a list of document IDs

        Returns
        -------
        List[int]
            a list containing the updated document's ID
        """
        timestamp = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()

        # Define the function that will perform the update
        if callable(fields):
            def perform_update(table: dict, doc_id: int) -> None:
                # Update documents by calling the update function provided by the user
                created_at = table[doc_id][self.created_key]
                fields(table[doc_id])                                          # type: ignore[operator]
                table[doc_id].update({self.created_key: created_at, self.updated_key: timestamp})
        else:
            def perform_update(table: dict, doc_id: int) -> None:
                # Update documents by setting all fields from the provided data
                created_at = table[doc_id][self.created_key]
                table[doc_id].update(fields)
                table[doc_id].update({self.created_key: created_at, self.updated_key: timestamp})

        if doc_ids is not None:
            # Perform the update operation for documents specified by a list of document IDs

            updated_ids = list(doc_ids)

            def updater(table: dict) -> None:
                # Call the processing callback with all document IDs
                for doc_id in updated_ids:
                    perform_update(table, doc_id)

            # Perform the update operation (see _update_table for details)
            self._update_table(updater)

            return updated_ids

        if cond is not None:
            # Perform the update operation for documents specified by a query

            # Collect affected doc_ids
            updated_ids = []

            def updater(table: dict) -> None:                              # pylint: disable=function-redefined
                _cond = cast('Query', cond)

                # We need to convert the keys iterator to a list because we may remove entries from the
                # ``table`` dict during iteration and doing this without the list conversion would result in an
                # exception (RuntimeError: dictionary changed size during iteration)
                for doc_id in list(table.keys()):
                    # Pass through all documents to find documents matching the
                    # query. Call the processing callback with the document ID
                    if _cond(table[doc_id]):
                        # Add ID to list of updated documents
                        updated_ids.append(doc_id)

                        # Perform the update (see above)
                        perform_update(table, doc_id)

            # Perform the update operation (see _update_table for details)
            self._update_table(updater)

            return updated_ids

        # Update all documents unconditionally

        updated_ids = []

        def updater(table: dict) -> None:    # type: ignore[no-redef]      # pylint: disable=function-redefined
            # Process all documents
            for doc_id in list(table.keys()):
                # Add ID to list of updated documents
                updated_ids.append(doc_id)

                # Perform the update (see above)
                perform_update(table, doc_id)

        # Perform the update operation (see _update_table for details)
        self._update_table(updater)

        return updated_ids

    def update_multiple(
        self,
        updates: Iterable[
            Tuple[Union[Mapping, Callable[[Mapping], None]], Query]
        ],
    ) -> List[int]:
        """Update all matching documents to have a given set of fields.

        Parameters
        ----------
        updates
            TODO

        .. todo:: Parameter description

        Returns
        -------
        List[int]
            a list containing the updated document's ID
        """
        timestamp = datetime.utcnow().replace(tzinfo=timezone.utc).isoformat()

        # Define the function that will perform the update
        def perform_update(
                fields: Union[Mapping, Callable[[Mapping], None]],
                table: dict,
                doc_id: int) -> None:
            if callable(fields):
                # Update documents by calling the update function provided by the user
                created_at = table[doc_id][self.created_key]
                fields(table[doc_id])
                table[doc_id].update({self.created_key: created_at, self.updated_key: timestamp})
            else:
                # Update documents by setting all fields from the provided
                # data
                created_at = table[doc_id][self.created_key]
                table[doc_id].update(fields)
                table[doc_id].update({self.created_key: created_at, self.updated_key: timestamp})

        # Perform the update operation for documents specified by a query

        # Collect affected doc_ids
        updated_ids = []

        def updater(table: dict) -> None:
            # We need to convert the keys iterator to a list because we may remove entries from the ``table``
            # dict during iteration and doing this without the list conversion would result in an exception
            # (RuntimeError: dictionary changed size during iteration)
            for doc_id in list(table.keys()):
                for fields, cond in updates:
                    _cond = cast('Query', cond)

                    # Pass through all documents to find documents matching the
                    # query. Call the processing callback with the document ID
                    if _cond(table[doc_id]):
                        # Add ID to list of updated documents
                        updated_ids.append(doc_id)

                        # Perform the update (see above)
                        perform_update(fields, table, doc_id)

        # Perform the update operation (see _update_table for details)
        self._update_table(updater)

        return updated_ids


class TableUuidTimestamp(TableUuid, TableTimestamp):
    """A table class with timestamps and UUID as ``doc_id``."""
