import random
import itertools
import bisect

def generate_haystack(given_name_candidates, family_name_candidates, elem_count):
    # Make different names have different probabilities
    given_name_weights = [ random.random() for unused in given_name_candidates ]
    family_name_weights = [ random.random() for unused in family_name_candidates ]
    # Based on random.choices of Python 3.6
    given_name_cumul_weights = list(itertools.accumulate(given_name_weights))
    family_name_cumul_weights = list(itertools.accumulate(family_name_weights))
    given_name_total_weight = given_name_cumul_weights[-1]
    family_name_total_weight = family_name_cumul_weights[-1]
    haystack = ['%s, %s' % (family_name_candidates[bisect.bisect(family_name_cumul_weights, random.random() * family_name_total_weight)],
                            given_name_candidates[bisect.bisect(given_name_cumul_weights, random.random() * given_name_total_weight)])
                for i in range(elem_count)]
    haystack.sort()
    return haystack

def generate_pages(data, pagesize, truncation_lengths):
    pages = []
    pagecount = 0
    trunc_len = 3
    for i in range(0, len(data), pagesize):
        page = {}
        page['id'] = pagecount
        pagecount += 1
        page['contents'] = data[i:i+pagesize]
        stats = {}
        stats['full'] = {}
        stats['full']['min'] = min(page['contents'])
        stats['full']['max'] = max(page['contents'])
        for trunc_len in truncation_lengths:
            truncation = 'trunc_%d' % trunc_len
            stats[truncation] = {}
            if len(stats['full']['min']) > trunc_len:
                stats[truncation]['min'] = stats['full']['min'][:trunc_len]
            else:
                stats[truncation]['min'] = stats['full']['min']

            if len(stats['full']['max']) > trunc_len:
                stats[truncation]['max'] = stats['full']['max'][:trunc_len - 1] + chr(ord(stats['full']['max'][trunc_len - 1]) + 1)
            else:
                stats[truncation]['max'] = stats['full']['max']
        page['stats'] = stats
        pages += [page]
    return pages
