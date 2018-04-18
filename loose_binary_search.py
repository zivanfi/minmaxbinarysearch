from common import *

# This algorithm does NOT require that for each page i:
#   "max value for page i" <= "min value for page i + 1"
#
# Instead, it requires that for each page i:
#   "min value for page i" <= "min value for page i + 1" and
#   "max value for page i" <= "max value for page i + 1"
# This is a looser condition that allows truncating min/max values.

def filter_pages(pages, needle, truncation):
    first_matching_page_lower_bound = last_matching_page_lower_bound = 0
    first_matching_page_upper_bound = last_matching_page_upper_bound = len(pages) - 1
    step_count = 0

    # Look for the first possibly matching page...
    found = False
    while not found:
        if first_matching_page_lower_bound > first_matching_page_upper_bound:
            break # No matching pages
        step_count += 1
        i = (first_matching_page_lower_bound + first_matching_page_upper_bound)//2
        if needle < pages[i]['stats'][truncation]['min']:
            first_matching_page_upper_bound = last_matching_page_upper_bound = i
        elif needle > pages[i]['stats'][truncation]['max']:
            first_matching_page_lower_bound = last_matching_page_lower_bound = i + 1
        else:
            first_matching_page_upper_bound = last_matching_page_lower_bound = i

        found = first_matching_page_lower_bound == first_matching_page_upper_bound

    if found:
        # Look for the last possibly matching page...
        found = False
        while not found:
            if last_matching_page_lower_bound > last_matching_page_upper_bound:
                break # No matching pages
            step_count += 1
            i = (last_matching_page_lower_bound + last_matching_page_upper_bound + 1)//2
            if needle < pages[i]['stats'][truncation]['min']:
                last_matching_page_upper_bound = i - 1
            else:
                last_matching_page_lower_bound = i

            found = last_matching_page_lower_bound == last_matching_page_upper_bound

    if found:
        # Check intersection of the two page ranges (from "first matching" and up to "last matching")
        found = first_matching_page_lower_bound <= last_matching_page_lower_bound

    if found:
        # Page interval [first_matching_page_lower_bound, last_matching_page_lower_bound match] matches
        number_of_matching_pages = last_matching_page_lower_bound - first_matching_page_lower_bound + 1
        # Sanity check
        assert not contains_value(pages[:first_matching_page_lower_bound], needle)
        assert not contains_value(pages[last_matching_page_lower_bound + 1:], needle)
    else:
        # No pages match
        number_of_matching_pages = 0
        # Sanity check
        assert not contains_value(pages, needle)

    return number_of_matching_pages, step_count
