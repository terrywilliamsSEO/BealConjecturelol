# Small-Prime Sensitivity For `(5,4,5)`

This report checks whether the current trace mismatch is driven by the smallest good primes.

| profile | primes used | surviving | eliminated | first eliminators | label | q=3 only |
| --- | --- | ---: | ---: | --- | --- | --- |
| `exclude_q_3` | `7;13;17;19;23;29;31;37;41;43;47;53;59;61;67;71;73;79;83;89;97` | 0 | 2 | `newform_0:q=17;newform_1:q=13` | `trace_mismatch_candidate` | `False` |
| `exclude_q_3_7` | `13;17;19;23;29;31;37;41;43;47;53;59;61;67;71;73;79;83;89;97` | 0 | 2 | `newform_0:q=17;newform_1:q=13` | `trace_mismatch_candidate` | `False` |
| `exclude_q_lt_11` | `13;17;19;23;29;31;37;41;43;47;53;59;61;67;71;73;79;83;89;97` | 0 | 2 | `newform_0:q=17;newform_1:q=13` | `trace_mismatch_candidate` | `False` |
| `exclude_q_lt_17` | `17;19;23;29;31;37;41;43;47;53;59;61;67;71;73;79;83;89;97` | 1 | 1 | `newform_0:q=17` | `trace_survivor_exists` | `False` |
| `use_only_q_ge_17` | `17;19;23;29;31;37;41;43;47;53;59;61;67;71;73;79;83;89;97` | 1 | 1 | `newform_0:q=17` | `trace_survivor_exists` | `False` |

Interpretation: if removing `q=3` restores a survivor, the safe label is `small_prime_dependent`. If the mismatch survives using only `q >= 17`, the safe label is `robust_trace_mismatch_candidate`.
