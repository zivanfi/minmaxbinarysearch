# minmaxbinarysearch

## Background

### `min_value` and `max_value`

The specification for the `min_value` and `max_value` fields of Parquet allows
these values to be different from the actual smallest and largest numbers as
long as the real-min to real-max range is contained within the `min_value` to
`max_value` range. In other words, the `min_value` to `max_value` range does not
have to fit tightly around the data, but it can be made broader instead.

This definition allows truncating the `min_value` and `max_value` fields. For
example, suppose a page contains the following two values:

* "Blart Versenwald III"
* "Slartibartfast"

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
looser condition that the list of `min_values` and the list of `max_values`
remain sorted _separately, irrespective to each other_. For example:

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

The script generates multiple datasets by picking random names from a fixed set
of candidates with random weights. A given name and a family name is chosen
independently and concatenated to form a single value of the dataset. The values
are stored in pages that have a different random value count in every dataset.
Finally, another random name is chosen and the pages are searched for potential
matches.

Two metrics are collected:

* `steps`: The number of steps the search algorithm took.

* `matches`: The number of pages identified as potentially matching.

Two algorithms are compared:

* `strict`: The min and max values are the actual smallest and largest values of a
  page (respectively). The binary search builds on the assumption that
  * `min value for page i` <= `all values in page i` <= `max value for page i` and
  * `max value for page i` <= `min value for page i + 1`

* `loose`: The min/max values are allowed to be smaller/larger (respectively) than
  the actual smallest/largest (respectively) values of a page. The binary search
  builds on the looser assumption that:

  * `min value for page i` <= `all values in page i` <= `max value for page i` and
  * `min value for page i` <= `min value for page i + 1` and
  * `max value for page i` <= `max value for page i + 1`

  Since the loose algorithm allows truncation of min/max values, different
  truncation lengths are also compared.

Example output:

                                               metric:     steps     steps     steps     steps     steps             matches   matches   matches   matches   matches
                                            algorithm:    strict     loose     loose     loose     loose              strict     loose     loose     loose     loose
                                             stat len:       N/A      full  trunc_10   trunc_5   trunc_2                 N/A      full  trunc_10   trunc_5   trunc_2
     execution elemcount  pagesize pagecount
    ----------------------------------------------------------------------------------------------------------------------------------------------------------------
             0      5845      1000         6                   4         4         4         4         4                   1         1         1         1         1
             1      4507       100        46                   7         7         7         8         8                   1         1         1         2         3
             2      9064      1000        10                   4         5         5         5         5                   1         1         1         1         1
             3      9480      1000        10                   4         4         4         4         4                   1         1         1         1         1
             4      1620       100        17                   5         5         5         5         5                   1         1         1         1         1
             5       176        10        18                   5         5         5         5         6                   0         0         0         0         1
             6      3302      1000         4                   3         3         3         3         3                   1         1         1         1         1
             7      3586         2      1793                  12        12        12        16        16                   0         0         1         5        18
             8      4908         2      2454                  12        12        12        14        16                   0         0         1         3        15
             9      5691       100        57                   7         8         8         8         8                   1         1         1         1         1
            10      5825      1000         6                   4         4         4         4         4                   1         1         1         1         1
            11      4215        10       422                  10        10        11        11        12                   1         1         2         2         5
            12      1883       100        19                   5         5         5         5         5                   1         1         1         1         1
            13      3742        10       375                   9        10        10        10        10                   1         1         1         1         1
            14      3651        10       366                  10        10        10        11        14                   0         0         0         2        11
            15      5398         2      2699                  12        17        17        17        18                   1         1        13        13       121
            16      3565        10       357                  10        10        10        10        14                   1         1         1         1        11
            17      3582      1000         4                   3         3         3         3         3                   1         1         1         1         1
            18      9002         2      4501                  13        13        13        16        20                   0         0         0         5        60
            19      8914         2      4457                  13        13        13        13        16                   1         1         1         1         9
    [4980 executions omitted]
    ----------------------------------------------------------------------------------------------------------------------------------------------------------------
       average                        747.44                7.73      7.99      8.20      9.03      9.91                0.86      0.86      1.34      3.66     12.89

The example above generated 5000 data sets and the last line shows that using
the same min and max values, the strict vs. the loose algorithm took 7.73 vs.
7.99 steps on average to execute. A truncation of the min/max values (only
allowed by the loose algorithm) to a length of 10, 5 and 2 characters increased
the average step count to 8.20, 9.03 and 9.91, respectively.

The last line of the example above also shows that on average, each data set
contained 747.44 pages. Using the same min and max values, both the strict and
the loose algorithms returned 0.86 potentially matching pages. A truncation of
the min/max values (only allowed by the loose algorithm) to a length of 10, 5
and 2 characters increased the number of pages returned to 1.34, 3.66 and 12.89,
respectively.

## Conclusion

As expected, the loose algorithm may take more steps and may return more
potential pages than the strict algorithm. However, the difference is not
significant enough to justify supporting both algorithms and the space saving
opportunities allowed by the loose algorithm easily outweigh its slight
performance disadvantage in my opinion.
