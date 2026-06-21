# Local Coverage Audit For `(5,4,5)`

The current good-prime trace comparison enumerates unit power-image triples. It assumes the selected prime does not divide `ABC`.

- Primes with local coverage gaps: `22` of `22`.

| q | unit residue cases | zero-support cases | power-image unit survivors | nonsingular Frey reductions | excluded cases | label |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 3 | 2 | 7 | 1 | 1 | 7 | `local_coverage_gap` |
| 7 | 30 | 19 | 15 | 15 | 19 | `local_coverage_gap` |
| 13 | 132 | 37 | 33 | 33 | 37 | `local_coverage_gap` |
| 17 | 240 | 49 | 60 | 60 | 49 | `local_coverage_gap` |
| 19 | 306 | 55 | 153 | 153 | 55 | `local_coverage_gap` |
| 23 | 462 | 67 | 231 | 231 | 67 | `local_coverage_gap` |
| 29 | 756 | 85 | 189 | 189 | 85 | `local_coverage_gap` |
| 31 | 750 | 211 | 15 | 15 | 211 | `local_coverage_gap` |
| 37 | 1260 | 109 | 315 | 315 | 109 | `local_coverage_gap` |
| 41 | 1400 | 281 | 14 | 14 | 281 | `local_coverage_gap` |
| 43 | 1722 | 127 | 861 | 861 | 127 | `local_coverage_gap` |
| 47 | 2070 | 139 | 1035 | 1035 | 139 | `local_coverage_gap` |
| 53 | 2652 | 157 | 663 | 663 | 157 | `local_coverage_gap` |
| 59 | 3306 | 175 | 1653 | 1653 | 175 | `local_coverage_gap` |
| 61 | 3300 | 421 | 33 | 33 | 421 | `local_coverage_gap` |
| 67 | 4290 | 199 | 2145 | 2145 | 199 | `local_coverage_gap` |
| 71 | 4550 | 491 | 91 | 91 | 491 | `local_coverage_gap` |
| 73 | 5112 | 217 | 1278 | 1278 | 217 | `local_coverage_gap` |
| 79 | 6006 | 235 | 3003 | 3003 | 235 | `local_coverage_gap` |
| 83 | 6642 | 247 | 3321 | 3321 | 247 | `local_coverage_gap` |
| 89 | 7656 | 265 | 1914 | 1914 | 265 | `local_coverage_gap` |
| 97 | 9120 | 289 | 2280 | 2280 | 289 | `local_coverage_gap` |

A `local_coverage_gap` means the trace packet still needs a human argument handling reductions with `q | A`, `q | B`, or `q | C`, or showing those cases are irrelevant for the intended good-prime comparison.
