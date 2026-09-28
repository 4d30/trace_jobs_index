#!/usr/bin/env python

#from itertools import repeat
#from datetime import datetime
#
#import xapian
#
#from .format import TEXT_FIELDS, DATA_FIELDS, SLOT_FIELDS, VIEW_FIELDS, PREFIXES, SLOT_VALUES
#
#from .transform import get_stemmer, get_termgen, get_queryparser
#
#
#
#def facet(doc, prefix, values):
#    if isinstance(values, str):
#        values = [values]
#
#    for v in values or []:
#        if not v:
#            continue
#
#        term = norm(v)
#        # Longest place name is 85 chars
#        if len(term) > 85:
#            continue
#        doc.add_term(f"{prefix}{term}")
#
#
#def index_document(xdb, content_hash, data):
#    doc = xapian.Document()
#
#    doc.set_data(content_hash)
#    doc.add_boolean_term(f"Q{content_hash}")
#
#    termgen = get_termgen()
#    termgen.set_document(doc)
#
#    text_fields = TEXT_FIELDS.intersection(data.keys())
#    for text_field in text_fields:
#        termgen.index_text(data[text_field], 1, PREFIXES[text_field])
#
#    data_fields = DATA_FIELDS.intersection(data.keys())
#    for data_field in data_fields:
#        facet(doc, PREFIXES[data_field], data[data_field])
#
#    slot_fields = SLOT_FIELDS.intersection(data.keys())
#    for slot_field in slot_fields:
#        if slot_field == 'date_posted':
#            value = datetime.strptime(data[slot_field], "%Y-%m-%d").timestamp()
#        else:
#            value = data[slot_field]
#        doc.add_value(SLOT_VALUES[slot_field],
#                      xapian.sortable_serialise(value))
#
#    xdb.replace_document(f"Q{content_hash}", doc)
#
#
## transform.py
# common
#def get_stemmer():
#    return xapian.Stem("en")
#
#
## for indexing documents
#def get_termgen():
#    termgen = xapian.TermGenerator()
#    termgen.set_stemmer(get_stemmer())
#    return termgen
#
#
## for locating documents
#def get_queryparser(db=None):
#    queryparser = xapian.QueryParser()
#    queryparser.set_stemmer(get_stemmer())
#    queryparser.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
#    if db is not None:
#        queryparser.set_database(db)
#    return queryparser
#
#
#mdet = LanguageDetectorBuilder.from_all_spoken_languages().build()

# format.py
#TEXT_FIELDS = set(('title', 'industry', 'company', 'location',))
#
#
#DATA_FIELDS = set(('employment_type', 'job_location_type',
#                   'language', 'det_language', 'country',
#                   'region', 'city', 'salary_currency',
#                   'url'))
#
#SLOT_FIELDS = set(('posted_after', 'posted_before', 'date_posted', 'salary_min', 'salary_max',))
#
#
#VIEW_FIELDS = set(('sortby', 'offset',))
#
#
#PREFIXES = {
#    'title': 'A',
#    'industry': 'B',
#    'company': 'C',
#    'employment_type': 'D',
#    'job_location_type': 'E',
#    'language': 'F',
#    'det_language': 'G',
#    'country': 'H',
#    'region': 'I',
#    'city': 'J',
#    'location': 'K',
#    'salary_currency': 'L',
#    'url': 'M',
#}
#
#SLOT_VALUES = {'date_posted': 0,
#               'posted_after': 0,
#               'posted_before': 0,
#               'salary_min': 1,
#               'salary_max': 2, }
#
#
##### engine.py
#def norm(v: str) -> str:
#    return (v.strip().lower().replace(" ", "_"))
#
#
#def make_query(data):
#    qp = get_queryparser()
#    text_fields = TEXT_FIELDS.intersection(data.keys())
#    Qs = []
#    Qs.append(xapian.Query.MatchAll)
#    for text_field in text_fields:
#        tfq = map(qp.parse_query,
#                  data[text_field],
#                  repeat(xapian.QueryParser.FLAG_DEFAULT),
#                  repeat(PREFIXES[text_field]))
#        tfq = xapian.Query(xapian.Query.OP_OR, tuple(tfq))
#        Qs.append(tfq)
#
#    data_fields = DATA_FIELDS.intersection(data.keys())
#    for data_field in data_fields:
#        normed = map(norm, data[data_field])
#        dfq = map(''.join, zip(repeat(PREFIXES[data_field]), normed))
#        dfq = map(xapian.Query, dfq)
#        dfq = xapian.Query(xapian.Query.OP_OR, tuple(dfq))
#        Qs.append(dfq)
#
#    slot_fields = SLOT_FIELDS.intersection(data.keys())
#    for slot_field in slot_fields:
#        if slot_field == 'posted_after':
#            value = datetime.strptime(data[slot_field], "%Y-%m-%d").timestamp()
#            value = xapian.sortable_serialise(value)
#            sfq = xapian.Query(xapian.Query.OP_VALUE_GE,
#                               SLOT_VALUES[slot_field],
#                               value)
#            Qs.append(sfq)
#        elif slot_field == 'salary_min':
#            value = xapian.sortable_serialise(data[slot_field])
#            max_salary = SLOT_VALUES['salary_max']
#            sfq = xapian.Query(xapian.Query.OP_VALUE_GE, max_salary, value)
#            Qs.append(sfq)
#        elif slot_field == 'salary_max':
#            value = xapian.sortable_serialise(data[slot_field])
#            min_salary = SLOT_VALUES['salary_min']
#            sfq = xapian.Query(xapian.Query.OP_VALUE_LE, min_salary, value)
#            Qs.append(sfq)
#    return xapian.Query(xapian.Query.OP_AND, tuple(Qs))


#def transform(record):
#    acc = {}
#    if 'title' in record:
#        acc['title'] = record['title']
#    if 'employmentType' in record:
#        acc['employment_type'] = record['employmentType']
#    if 'jobLocationType' in record:
#        acc['job_location_type'] = record['jobLocationType']
#    if 'inLanguage' in record:
#        acc['language'] = record['inLanguage']
#    if 'industry' in record:
#        acc['industry'] = record['industry']
#    if 'hiringOrganization' in record:
#        if 'name' in record['hiringOrganization']:
#            acc['company'] = record['hiringOrganization']['name']
#    if 'datePosted' in record:
#        acc['date_posted'] = record['datePosted']
#    if 'url' in record:
#        acc['url'] = record['url']
#    if 'jobLocation' in record:
#        if 'location' not in acc:
#            acc['location'] = ""
#        for location in record['jobLocation']:
#            if 'address' in location:
#                if isinstance(location['address'], dict):
#                    if 'addressLocality' in location['address']:
#                        if 'city' not in acc:
#                            acc['city'] = []
#                        acc['city'].append(location['address']['addressLocality'])
#                        acc['location'] = ' '.join([acc['location'], location['address']['addressLocality']])
#                    if 'addressRegion' in location['address']:
#                        if 'region' not in acc:
#                            acc['region'] = []
#                        acc['region'].append(location['address']['addressRegion'])
#                        acc['location'] = ' '.join([acc['location'], location['address']['addressRegion']])
#                    if 'addressCountry' in location['address']:
#                        if 'country' not in acc:
#                            acc['country'] = []
#                        acc['country'].append(location['address']['addressCountry'])
#                        acc['location'] = ' '.join([acc['location'], location['address']['addressCountry']])
#                elif isinstance(location['address'], str):
#                    acc['location'] = ' '.join([acc['location'], location['address']])
#    if 'baseSalary' in record:
#        if 'currency' in record['baseSalary']:
#            acc['salary_currency'] = record['baseSalary']['currency']
#        if 'value' in record['baseSalary']:
#            if 'minValue' in record['baseSalary']['value']:
#                acc['salary_min'] = record['baseSalary']['value']['minValue']
#            if 'maxValue' in record['baseSalary']['value']:
#                acc['salary_max'] = record['baseSalary']['value']['maxValue']
#    return acc
#
