#!/usr/bin/env python

import os

import xapian

from . import cafs, transform

from .format import TEXT_FIELDS, DATA_FIELDS, SLOT_FIELDS, SLOT_VALUES, PREFIXES

def facet(doc, prefix, values):
    if isinstance(values, str):
        values = [values]

    for v in values or []:
        if not v:
            continue

        term = norm(v)
        # Longest place name is 85 chars
        if len(term) > 85:
            continue
        doc.add_term(f"{prefix}{term}")


def index_document(xdb, content_hash, data):
    doc = xapian.Document()

    doc.set_data(content_hash)
    doc.add_boolean_term(f"Q{content_hash}")

    termgen = transform.get_termgen()
    termgen.set_document(doc)

    text_fields = TEXT_FIELDS.intersection(data.keys())
    for text_field in text_fields:
        termgen.index_text(data[text_field], 1, PREFIXES[text_field])

    data_fields = DATA_FIELDS.intersection(data.keys())
    for data_field in data_fields:
        facet(doc, PREFIXES[data_field], data[data_field])

    slot_fields = SLOT_FIELDS.intersection(data.keys())
    for slot_field in slot_fields:
        if slot_field == 'date_posted':
            value = datetime.strptime(data[slot_field], "%Y-%m-%d").timestamp()
        else:
            value = data[slot_field]
        doc.add_value(SLOT_VALUES[slot_field],
                      xapian.sortable_serialise(value))

    xdb.replace_document(f"Q{content_hash}", doc)


def synchronize(rebuild=False):
    xdb = xapian.WritableDatabase(os.getenv('XAPIAN_ROOT'),
                                  xapian.DB_CREATE_OR_OPEN)
    walk = cafs.walk(cafs_root=os.getenv('CAFS_ROOT'))
    for file in walk:
        content_hash = os.path.basename(file)
        if xdb.term_exists(f"Q{content_hash}") and not rebuild:
            continue
        data = cafs.get(content_hash, cafs_root=os.getenv('CAFS_ROOT'))
        doc = transform.flatten_record(data)
        index_document(xdb, content_hash, doc)
