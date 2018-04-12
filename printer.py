def print_padded_string(val):
   print('%10s' % val, end = '')

def print_padded_integer(val):
   print('%10d' % val, end = '')

def print_padded_float(val):
   print('%10.2f' % val, end = '')

def print_table_header(truncation_lengths):
    print_padded_string('')
    print_padded_string('')
    print_padded_string('')
    print_padded_string('')
    print_padded_string('')
    print_padded_string('steps')
    for i in truncation_lengths:
        print_padded_string('steps')
    print('%20s' % 'matches', end = '')
    for i in truncation_lengths:
        print_padded_string('matches')
    print()

    print_padded_string('execution')
    print_padded_string('elemcount')
    print_padded_string('pagesize')
    print_padded_string('pagecount')
    print_padded_string('')
    print_padded_string('(full)')
    for i in truncation_lengths:
        truncation = '(trunc%d)' % i
        print_padded_string(truncation)
    print_padded_string('')
    print_padded_string('(full)')
    for i in truncation_lengths:
        truncation = '(trunc%d)' % i
        print_padded_string(truncation)
    print()
    print('-' * 140)
