import random

def generate_haystack(haystack_candidates, elem_count):
    haystack = []
    for i in range(0, elem_count):
        haystack += [random.choice(haystack_candidates)]
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
            truncation = 'truncated_to_%d' % trunc_len
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
