#!/usr/bin/env python


# from selectolax.lexbor import LexborHTMLParser
import xapian


# common
def get_stemmer():
    return xapian.Stem("en")


# for indexing documents
def get_termgen():
    termgen = xapian.TermGenerator()
    termgen.set_stemmer(get_stemmer())
    return termgen


# for locating documents
def get_queryparser(db=None):
    queryparser = xapian.QueryParser()
    queryparser.set_stemmer(get_stemmer())
    queryparser.set_stemming_strategy(xapian.QueryParser.STEM_SOME)
    if db is not None:
        queryparser.set_database(db)
    return queryparser


def flatten_record(record):
    acc = {}
    if 'title' in record:
        acc['title'] = record['title']
    if 'employmentType' in record:
        acc['employment_type'] = record['employmentType']
    if 'jobLocationType' in record:
        acc['job_location_type'] = record['jobLocationType']
    if 'inLanguage' in record:
        acc['language'] = record['inLanguage']
    if 'industry' in record:
        acc['industry'] = record['industry']
    if 'hiringOrganization' in record:
        if 'name' in record['hiringOrganization']:
            acc['company'] = record['hiringOrganization']['name']
    if 'datePosted' in record:
        acc['date_posted'] = record['datePosted']
    if 'url' in record:
        acc['url'] = record['url']
    if 'jobLocation' in record:
        if 'location' not in acc:
            acc['location'] = ""
        for location in record['jobLocation']:
            if 'address' in location:
                if isinstance(location['address'], dict):
                    if 'addressLocality' in location['address']:
                        if 'city' not in acc:
                            acc['city'] = []
                        acc['city'].append(location['address']['addressLocality'])
                        acc['location'] = ' '.join([acc['location'], location['address']['addressLocality']])
                    if 'addressRegion' in location['address']:
                        if 'region' not in acc:
                            acc['region'] = []
                        acc['region'].append(location['address']['addressRegion'])
                        acc['location'] = ' '.join([acc['location'], location['address']['addressRegion']])
                    if 'addressCountry' in location['address']:
                        if 'country' not in acc:
                            acc['country'] = []
                        acc['country'].append(location['address']['addressCountry'])
                        acc['location'] = ' '.join([acc['location'], location['address']['addressCountry']])
                elif isinstance(location['address'], str):
                    acc['location'] = ' '.join([acc['location'], location['address']])
    if 'baseSalary' in record:
        if 'currency' in record['baseSalary']:
            acc['salary_currency'] = record['baseSalary']['currency']
        if 'value' in record['baseSalary']:
            if 'minValue' in record['baseSalary']['value']:
                acc['salary_min'] = record['baseSalary']['value']['minValue']
            if 'maxValue' in record['baseSalary']['value']:
                acc['salary_max'] = record['baseSalary']['value']['maxValue']
    return acc


def norm(v: str) -> str:
    return (v.strip().lower().replace(" ", "_"))
