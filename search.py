#!/usr/bin/env python

#import os
#from datetime import datetime, timedelta
#
#import xapian
#
#from . import model
#
#
#def search(data):
    #query = model.make_query(data['search'])
    #xdb = xapian.Database(os.getenv('XAPIAN_ROOT'), xapian.DB_OPEN)
    #inquiry = xapian.Enquire(xdb)
    #inquiry.set_query(query)
    #default_sort_slot = model.SLOT_VALUES['date_posted']
    #inquiry.set_sort_by_relevance_then_value(default_sort_slot, True)
    #offset = 0
    #view_fields = model.VIEW_FIELDS.intersection(data['view'].keys())
    #for view_field in view_fields:
        #match view_field:
            #case 'sortby':
                #match data['view'][view_field]:
                    #case 'bm25':
                        #pass
                    #case 'date_posted':
                        #slot = model.SLOT_VALUES['date_posted']
                        #inquiry.set_sort_by_value(slot, True)
                    #case 'salary_min':
                        #slot = model.SLOT_VALUES['salary_min']
                        #inquiry.set_sort_by_value(slot, True)
                    #case 'salary_max':
                        #slot = model.SLOT_VALUES['salary_max']
                        #inquiry.set_sort_by_value(slot, True)
            #case 'offset':
                #offset = int(data['view']['offset'])
    #mset = inquiry.get_mset(offset, 12)
    #hashes = tuple(m.document.get_data().decode('utf-8') for m in mset)
    #xdb.close()
    #return hashes
#
#
#def _get_window(date):
    #dt = datetime.strptime(date, '%Y-%m-%d')
    #dt1 = (dt - timedelta(days=1)).timestamp()
    #dt30 = (dt - timedelta(days=30)).timestamp()
    #return dt30, dt1
#
#
## def get_date(language, date):
##     xdb = xapian.Database(os.getenv('XAPIAN_ROOT'), xapian.DB_OPEN)
##     n_docs = xdb.get_doccount()
##     pfx_l = index_model.PREFIXES['det_language']
##     q_lang = f'{pfx_l}_{language}'
##     ql = xapian.Query(q_lang)
##     dt0 = datetime.strptime(date, '%Y-%m-%d')
##     dt1 = (dt0 + timedelta(days=1)).timestamp()
##     dt0 = dt0.timestamp()
##     qd = xapian.Query(xapian.Query.OP_VALUE_RANGE, 0,
##                       xapian.sortable_serialise(dt0),
##                       xapian.sortable_serialise(dt1))
##     query = xapian.Query(xapian.Query.OP_FILTER, ql, qd)
##     inquiry = xapian.Enquire(xdb)
##     inquiry.set_query(query)
##     mset = inquiry.get_mset(0, n_docs)
##     match_ids = (m.docid for m in mset)
##     docs = (xdb.get_document(mid) for mid in match_ids)
##     hashes = (d.get_data() for d in docs)
##     hashes = tuple(set(h.decode('utf-8') for h in hashes))
##     xdb.close()
##     return hashes
##
## def get_slice(language, date):
##     pfx_l = index_model.PREFIXES['det_language']
##     q_lang = f'{pfx_l}_{language}'
##     dt30, dt1 = _get_window(date)
##     ql = xapian.Query(q_lang)
##     qd = xapian.Query(xapian.Query.OP_VALUE_RANGE, 0,
##                       xapian.sortable_serialise(dt30),
##                       xapian.sortable_serialise(dt1))
##     query = xapian.Query(xapian.Query.OP_FILTER, ql, qd)
##
##     xdb = xapian.Database(os.getenv('XAPIAN_ROOT'), xapian.DB_OPEN)
##     n_docs = xdb.get_doccount()
##     inquiry = xapian.Enquire(xdb)
##     inquiry.set_query(query)
##     mset = inquiry.get_mset(0, n_docs)
##     match_ids = (m.docid for m in mset)
##     docs = (xdb.get_document(mid) for mid in match_ids)
##     hashes = (d.get_data() for d in docs)
##     hashes = tuple(set(h.decode('utf-8') for h in hashes))
##     xdb.close()
##     return hashes
#
#
#def date_generator():
    #from operator import mul, methodcaller
    #from itertools import repeat
    #day_per_year = 365.2425
    #ten_year = int(day_per_year * 10)
    #ten_years_ago = (datetime.now() - timedelta(days=ten_year)).timestamp()
    #today = datetime.now().timestamp()
    #sec_per_day = 86400
    #day_per_year = 365.2425
    #n_years = 100
    #n_days = int(mul(day_per_year, n_years))
    #days = range(n_days)
    #seconds = map(mul, repeat(sec_per_day), days)
    #seconds = filter(lambda x: x < today, seconds)
    #seconds = filter(lambda x: x > ten_years_ago, seconds)
    #datetimes = map(datetime.fromtimestamp, seconds)
    #dates = map(methodcaller('strftime', '%Y-%m-%d'), datetimes)
    #yield from dates
#
#
#isocodes = {
  #"aa", "ab", "ae", "af", "ak", "am", "an", "ar", "as", "av", "ay", "az",
  #"ba", "be", "bg", "bi", "bm", "bn", "bo", "br", "bs",
  #"ca", "ce", "ch", "co", "cr", "cs", "cu", "cv", "cy",
  #"da", "de", "dv", "dz",
  #"ee", "el", "en", "eo", "es", "et", "eu",
  #"fa", "ff", "fi", "fj", "fo", "fr", "fy",
  #"ga", "gd", "gl", "gn", "gu", "gv",
  #"ha", "he", "hi", "ho", "hr", "ht", "hu", "hy", "hz",
  #"ia", "id", "ie", "ig", "ii", "ik", "io", "is", "it", "iu",
  #"ja", "jv", "ka",
  #"kg", "ki", "kj", "kk", "kl", "km", "kn", "ko", "kr", "ks", "ku", "kv",
  #"kw", "ky",
  #"la", "lb", "lg", "li", "ln", "lo", "lt", "lu", "lv",
  #"mg", "mh", "mi", "mk", "ml", "mn", "mr", "ms", "mt", "my",
  #"na", "nb", "nd", "ne", "ng", "nl", "nn", "no", "nr", "nv", "ny", "oc",
  #"oj", "om", "or", "os",
  #"pa", "pi", "pl", "ps", "pt",
  #"qu",
  #"rm", "rn", "ro", "ru", "rw",
  #"sa", "sc", "sd", "se", "sg", "si", "sk", "sl", "sm", "sn", "so", "sq",
  #"sr", "ss", "st", "su", "sv", "sw",
  #"ta", "te", "tg", "th", "ti", "tk", "tl", "tn", "to", "tr", "ts", "tt",
  #"tw", "ty",
  #"ug", "uk", "ur", "uz",
  #"ve", "vi", "vo",
  #"wa", "wo",
  #"xh",
  #"yi", "yo",
  #"za", "zh", "zu",
#}
#
#
#def language_generator():
    #import string
    #from itertools import product
    #chars = product(string.ascii_lowercase, repeat=2)
    #lang_codes = map(''.join, chars)
    #lang_codes = filter(lambda x: x in isocodes, lang_codes)
    #yield from lang_codes
#
#
#def main():
    #pass
#
#
#if __name__ == '__main__':
    #main()
