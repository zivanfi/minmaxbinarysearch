# minmaxbinarysearch

## Background

### `min_value` and `max_value`

The specification for the `min_value` and `max_value` fields of Parquet allows
these values to be different from the actual smallest and largest numbers as
long as the real-min to real-max range is contained within the `min_value` to
`max_value` range. In other words, the `min_value` to `max_value` range must not
tightly fit around the data, but it can be made larger instead.

This allows truncating values. For example, suppose a page contains the
following two values:

* Blart Versenwald III
* Slartibartfast

In this case, the smallest value is "Blart Versenwald III", but the
`min_value` field can store a shorter string than that. A simple truncation
gives a valid `min_value`, to name a few possibilites, one may use "Bla", "Bl"
or "B".

The largest value is "Slartibartfast". This can also be shortened, but special
care must be taken to make this shorter value larger than the actual value. A
few feasible choices for `max_value` are: "Slb", "Sm" or "T".

### Sorted data

If data is sorted, the actual min and max values will naturally be sorted as
well. This property, however, is not true for shortened values. On the other
hand, if the shortening is done consistently, it is very easy to achieve a
looser condition as follows: the list of `min_values` can keep the correct order
and the list of `max_values` can also keep the correct order. For example:

Values     | `min_value` | `max_value`
-----------|-------------|-------------
Ann, Ann   | A           | B
Ann, Bob   | A           | C
Bob, Cindy | B           | D
Cindy, Ed  | C           | F
Ed, Gus    | E           | H
Gus        | G           | H

## The purpose of this project

This project is meant to demonstrate that filtering pages can be done
efficiently based on the `min_value` and `max_value` fields as described above.
In fact, a filtering algorithm based on having lists of `min_value` and
`max_value` fields that are sorted separately can be almost as efficient as if
those lists were also sorted in respect to the values from the other list.

Example output:

    Looking for existing values:
                                                           steps     steps     steps     steps             matches   matches   matches   matches
     execution elemcount  pagesize pagecount              (full)  (trunc3)  (trunc2)  (trunc1)              (full)  (trunc3)  (trunc2)  (trunc1)
    --------------------------------------------------------------------------------------------------------------------------------------------
             0      3600        10       360                  15        15        15        15                  18        18        18        37
             1      1324        10       133                  11        11        11        12                   7         7         7        14
             2      9637         2      4819                  20        20        20        22                 262       262       262       495
             3      7518      1000         8                   4         5         5         5                   1         1         1         1
             4      2609        10       261                  12        12        12        14                  17        17        17        29
             5      7535       100        76                   9         9         9         9                   5         5         5         5
             6       126      1000         1                   2         2         2         2                   1         1         1         1
             7      4502      1000         5                   4         4         4         4                   1         1         1         1
             8      2240      1000         3                   3         3         3         3                   1         1         1         1
             9      6598       100        66                  10        10        10        10                   5         5         5         8
    [4990 executions omitted]
    --------------------------------------------------------------------------------------------------------------------------------------------
       average                                             10.90     11.02     11.07     11.29               39.35     39.35     43.67     59.18
    
    Looking for non-existing values:
                                                           steps     steps     steps     steps             matches   matches   matches   matches
     execution elemcount  pagesize pagecount              (full)  (trunc3)  (trunc2)  (trunc1)              (full)  (trunc3)  (trunc2)  (trunc1)
    --------------------------------------------------------------------------------------------------------------------------------------------
             0      9428      1000        10                   5         5         5         6                   1         1         1         2
             1      1688        10       169                   9         9         9        12                   0         0         0        10
             2       448         2       224                   8        10        13        13                   1         1        15        15
             3       142       100         2                   2         2         2         2                   1         1         1         1
             4      8265        10       827                  11        11        11        16                   0         0         0        45
             5      3825      1000         4                   3         3         3         3                   1         1         1         1
             6      7688        10       769                  11        11        11        11                   1         1         1         1
             7      2490         2      1245                  11        11        11        11                   1         1         1         1
             8      8702        10       871                  11        11        11        16                   0         0         0        47
             9       760       100         8                   4         4         4         4                   0         0         0         1
    [4990 executions omitted]
    --------------------------------------------------------------------------------------------------------------------------------------------
       average                                             18.75     19.03     20.54     21.38               40.03     40.03     59.80     91.52
