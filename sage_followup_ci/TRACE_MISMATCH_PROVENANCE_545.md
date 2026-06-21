# Trace Mismatch Provenance For `(5,4,5)`

This report records where the current level-220 trace filter survives or eliminates each newform slot. It is an audit artifact only.

## Newform `0`

- First eliminating prime: `3`.
- All eliminating primes: `3;17;41;61`.

| q | a_q | Frey traces | mode | classification | first eliminator |
| ---: | --- | --- | --- | --- | --- |
| 3 | `-2` | `0` | `mod_5` | `eliminated` | `True` |
| 7 | `-4` | `-4;0;4` | `exact` | `survives` | `False` |
| 13 | `-4` | `-6;-2;2;6` | `mod_5` | `survives` | `False` |
| 17 | `0` | `-6;-2;2;6` | `mod_5` | `eliminated` | `False` |
| 19 | `-4` | `-8;-4;0;4;8` | `exact` | `survives` | `False` |
| 23 | `-6` | `-8;-4;0;4;8` | `mod_5` | `survives` | `False` |
| 29 | `-6` | `-10;-6;-2;2;6;10` | `exact` | `survives` | `False` |
| 31 | `8` | `-8;-4;0;4;8` | `exact` | `survives` | `False` |
| 37 | `2` | `-10;-6;-2;2;6;10` | `exact` | `survives` | `False` |
| 41 | `6` | `-6;2;10` | `mod_5` | `eliminated` | `False` |
| 43 | `8` | `-12;-8;-4;0;4;8;12` | `exact` | `survives` | `False` |
| 47 | `6` | `-12;-8;-4;0;4;8;12` | `mod_5` | `survives` | `False` |
| 53 | `-6` | `-14;-10;-6;-2;2;6;10;14` | `exact` | `survives` | `False` |
| 59 | `-12` | `-12;-8;-4;0;4;8;12` | `exact` | `survives` | `False` |
| 61 | `2` | `-2;6;10;14` | `mod_5` | `eliminated` | `False` |
| 67 | `-10` | `-16;-12;-8;-4;0;4;8;12;16` | `mod_5` | `survives` | `False` |
| 71 | `-12` | `-16;-12;-8;-4;0;4;8;12;16` | `exact` | `survives` | `False` |
| 73 | `-16` | `-14;-10;-6;-2;2;6;10;14` | `mod_5` | `survives` | `False` |
| 79 | `8` | `-16;-12;-8;-4;0;4;8;12;16` | `exact` | `survives` | `False` |
| 83 | `0` | `-16;-12;-8;-4;0;4;8;12;16` | `exact` | `survives` | `False` |
| 89 | `6` | `-18;-14;-10;-6;-2;2;6;10;14;18` | `exact` | `survives` | `False` |
| 97 | `14` | `-18;-14;-10;-6;-2;2;6;10;14;18` | `exact` | `survives` | `False` |

## Newform `1`

- First eliminating prime: `3`.
- All eliminating primes: `3;13`.

| q | a_q | Frey traces | mode | classification | first eliminator |
| ---: | --- | --- | --- | --- | --- |
| 3 | `2` | `0` | `mod_5` | `eliminated` | `True` |
| 7 | `0` | `-4;0;4` | `exact` | `survives` | `False` |
| 13 | `0` | `-6;-2;2;6` | `mod_5` | `eliminated` | `False` |
| 17 | `-4` | `-6;-2;2;6` | `mod_5` | `survives` | `False` |
| 19 | `-4` | `-8;-4;0;4;8` | `exact` | `survives` | `False` |
| 23 | `6` | `-8;-4;0;4;8` | `mod_5` | `survives` | `False` |
| 29 | `2` | `-10;-6;-2;2;6;10` | `exact` | `survives` | `False` |
| 31 | `0` | `-8;-4;0;4;8` | `exact` | `survives` | `False` |
| 37 | `-6` | `-10;-6;-2;2;6;10` | `exact` | `survives` | `False` |
| 41 | `-10` | `-6;2;10` | `mod_5` | `survives` | `False` |
| 43 | `4` | `-12;-8;-4;0;4;8;12` | `exact` | `survives` | `False` |
| 47 | `10` | `-12;-8;-4;0;4;8;12` | `mod_5` | `survives` | `False` |
| 53 | `2` | `-14;-10;-6;-2;2;6;10;14` | `exact` | `survives` | `False` |
| 59 | `-4` | `-12;-8;-4;0;4;8;12` | `exact` | `survives` | `False` |
| 61 | `-14` | `-2;6;10;14` | `mod_5` | `survives` | `False` |
| 67 | `2` | `-16;-12;-8;-4;0;4;8;12;16` | `mod_5` | `survives` | `False` |
| 71 | `4` | `-16;-12;-8;-4;0;4;8;12;16` | `exact` | `survives` | `False` |
| 73 | `-4` | `-14;-10;-6;-2;2;6;10;14` | `mod_5` | `survives` | `False` |
| 79 | `-8` | `-16;-12;-8;-4;0;4;8;12;16` | `exact` | `survives` | `False` |
| 83 | `12` | `-16;-12;-8;-4;0;4;8;12;16` | `exact` | `survives` | `False` |
| 89 | `6` | `-18;-14;-10;-6;-2;2;6;10;14;18` | `exact` | `survives` | `False` |
| 97 | `6` | `-18;-14;-10;-6;-2;2;6;10;14;18` | `exact` | `survives` | `False` |

## Interpretation Boundary

The provenance label is computational route evidence. It does not certify the Frey attachment, conductor calculation, level lowering, residual irreducibility, or global exclusion step.
