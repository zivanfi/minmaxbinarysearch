def print_padded_string(val):
   print('%10s' % val, end = '')

def print_padded_integer(val):
   print('%10d' % val, end = '')

def print_padded_float(val):
   print('%10.2f' % val, end = '')

def print_table_header(truncations):
    print_padded_string('')
    print_padded_string('')
    print_padded_string('')
    print_padded_string('')
    print_padded_string('metric:')
    print_padded_string('steps')
    for i in truncations:
        print_padded_string('steps')
    print_padded_string('')
    print_padded_string('matches')
    for i in truncations:
        print_padded_string('matches')
    print()

    print_padded_string('')
    print_padded_string('')
    print_padded_string('')
    print_padded_string('')
    print_padded_string('algorithm:')
    print_padded_string('strict')
    for i in truncations:
        print_padded_string('loose')
    print_padded_string('')
    print_padded_string('strict')
    for i in truncations:
        print_padded_string('loose')
    print()

    print_padded_string('')
    print_padded_string('')
    print_padded_string('')
    print_padded_string('')
    print_padded_string('stat len:')
    print_padded_string('N/A')
    for selector in truncations:
        print_padded_string(selector)
    print_padded_string('')
    print_padded_string('N/A')
    for selector in truncations:
        print_padded_string(selector)
    print()

    print_padded_string('execution')
    print_padded_string('elemcount')
    print_padded_string('pagesize')
    print_padded_string('pagecount')
    print()
    print('-' * 10 * (8 + 2 * len(truncations)))
