# Candidate Comparison Levels For `(5,4,5)`

Level 220 is no longer treated as the only target. This table expands the possible lowered comparison levels from bad-prime exponent variants.

- Candidate count: `24`.
- Baseline level present: `True`.
- Variants without factor 11: `20;4;10;40;100;2;5;8;50;200;1;25`.
- Every row remains capped at `worth_human_modular_review`.

| level | factorization | e2 | e5 | e11 | includes 11 | score | label | reason |
| ---: | --- | ---: | ---: | ---: | --- | ---: | --- | --- |
| 20 | `2^2 * 5` | 2 | 1 | 0 | `False` | 8 | `plausible_without_11` | This level tests the route after removing the currently unjustified factor 11. |
| 4 | `2^2` | 2 | 0 | 0 | `False` | 7 | `plausible_without_11` | This level tests the route after removing the currently unjustified factor 11. |
| 10 | `2 * 5` | 1 | 1 | 0 | `False` | 7 | `plausible_without_11` | This level tests the route after removing the currently unjustified factor 11. |
| 40 | `2^3 * 5` | 3 | 1 | 0 | `False` | 7 | `plausible_without_11` | This level tests the route after removing the currently unjustified factor 11. |
| 100 | `2^2 * 5^2` | 2 | 2 | 0 | `False` | 7 | `plausible_without_11` | This level tests the route after removing the currently unjustified factor 11. |
| 220 | `2^2 * 5 * 11` | 2 | 1 | 1 | `True` | 7 | `current_baseline_heuristic` | Current level-220 route target retained as the baseline, but factor 11 remains unjustified. |
| 2 | `2` | 1 | 0 | 0 | `False` | 6 | `plausible_without_11` | This level tests the route after removing the currently unjustified factor 11. |
| 5 | `5` | 0 | 1 | 0 | `False` | 6 | `plausible_without_11` | This level tests the route after removing the currently unjustified factor 11. |
| 8 | `2^3` | 3 | 0 | 0 | `False` | 6 | `plausible_without_11` | This level tests the route after removing the currently unjustified factor 11. |
| 50 | `2 * 5^2` | 1 | 2 | 0 | `False` | 6 | `plausible_without_11` | This level tests the route after removing the currently unjustified factor 11. |
| 200 | `2^3 * 5^2` | 3 | 2 | 0 | `False` | 6 | `plausible_without_11` | This level tests the route after removing the currently unjustified factor 11. |
| 44 | `2^2 * 11` | 2 | 0 | 1 | `True` | 6 | `plausible_with_11` | This level keeps factor 11 as an exploratory variant pending conductor provenance. |
| 110 | `2 * 5 * 11` | 1 | 1 | 1 | `True` | 6 | `plausible_with_11` | This level keeps factor 11 as an exploratory variant pending conductor provenance. |
| 440 | `2^3 * 5 * 11` | 3 | 1 | 1 | `True` | 6 | `plausible_with_11` | This level keeps factor 11 as an exploratory variant pending conductor provenance. |
| 1100 | `2^2 * 5^2 * 11` | 2 | 2 | 1 | `True` | 6 | `plausible_with_11` | This level keeps factor 11 as an exploratory variant pending conductor provenance. |
| 1 | `1` | 0 | 0 | 0 | `False` | 5 | `exploratory_low_bad_prime_support` | Both 2 and 5 are absent, so this is a low-support exploratory comparison level. |
| 25 | `5^2` | 0 | 2 | 0 | `False` | 5 | `plausible_without_11` | This level tests the route after removing the currently unjustified factor 11. |
| 22 | `2 * 11` | 1 | 0 | 1 | `True` | 5 | `plausible_with_11` | This level keeps factor 11 as an exploratory variant pending conductor provenance. |
| 55 | `5 * 11` | 0 | 1 | 1 | `True` | 5 | `plausible_with_11` | This level keeps factor 11 as an exploratory variant pending conductor provenance. |
| 88 | `2^3 * 11` | 3 | 0 | 1 | `True` | 5 | `plausible_with_11` | This level keeps factor 11 as an exploratory variant pending conductor provenance. |
| 550 | `2 * 5^2 * 11` | 1 | 2 | 1 | `True` | 5 | `plausible_with_11` | This level keeps factor 11 as an exploratory variant pending conductor provenance. |
| 2200 | `2^3 * 5^2 * 11` | 3 | 2 | 1 | `True` | 5 | `plausible_with_11` | This level keeps factor 11 as an exploratory variant pending conductor provenance. |
| 11 | `11` | 0 | 0 | 1 | `True` | 4 | `exploratory_low_bad_prime_support` | Both 2 and 5 are absent, so this is a low-support exploratory comparison level. |
| 275 | `5^2 * 11` | 0 | 2 | 1 | `True` | 4 | `plausible_with_11` | This level keeps factor 11 as an exploratory variant pending conductor provenance. |

The scores are only triage weights for human review. They do not establish a conductor or lowered level.
