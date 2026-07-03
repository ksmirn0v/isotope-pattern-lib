# isotope-pattern-lib #

The library can be used to compute the isotope pattern
of a given molecular formula.

## Requirements ##

`python >= 3.9`

## Development ##

The project uses [`uv`](https://docs.astral.sh/uv/) as its package manager.

```
uv sync --group test --group dev
```

Run the test suite (unit and integration tests are run as separate `pytest`
invocations, so that mutated global state in one suite does not leak into the
other):

```
uv run pytest tests/unit
uv run pytest tests/integration
```

Build a distributable wheel/sdist:

```
uv build
```

## Usage ##

Although any of the classes/functions can be used independently,
the library has the main endpoints, located in
`isotope_pattern_lib/api.py`:
```
from isotope_pattern_lib import api
```
---
```
api.set_parser(config_path: str)
```
The call sets the parameters for parsing molecular formulas.
These parameters should be listed as elements with their corresponding isotopes
in a `yaml` file that is located in `config_path`.
The structure of the file will be described later.

The call is optional. If no call is conducted, a default parser is used.

---
```
def compute_isotope_pattern(formula_string: str)
```
The call computes isotope pattern of a given molecular formula, represented
as a string `formula_string` (_e.g._ `C2H5OH`).
The output represents a list of `IsotopeFormula` instances, each containing
the information on the constituent isotopes and the probability of the
associated compositions.

## YAML file structure ##

The YAML file is used to define the way how molecular formulas will be parsed.
It consists of a list of elements with the definition of the corresponding isotopes.
Each entry has the following form:
```
- name: string
  description: string
  isotopes:
    - name: string
      mass: float
      abundance: float
    - ...
- ...
```
**Comments**:

- The field `name` is arbitrary, but the raw strings that are used in the
`compute_isotope_pattern(formula_string: str)` call should not contain
any element names that are not part of the `name` fields, specified in the
`yaml` file.
- Each element can contain as many isotopes as it is wished.
- The field `abundance` should define a number less or equal to `1.0`.
However, these numbers, corresponding to different isotopes of an element,
  should not exceed in sum `1.0`.
  
## Default YAML file structure ##

```
- name: H
  description: hydrogen
  isotopes:
    - name: H1
      mass: 1.0078250
      abundance: 1.000
- name: C
  description: carbon
  isotopes:
    - name: C12
      mass: 12.0000000
      abundance: 0.989
    - name: C13
      mass: 13.0033548
      abundance: 0.011
- name: O
  description: oxygen
  isotopes:
    - name: O16
      mass: 15.9949146
      abundance: 0.998
    - name: O18
      mass: 17.9991596
      abundance: 0.002
- name: N
  description: nytrogen
  isotopes:
    - name: N14
      mass: 14.0030740
      abundance: 0.996
    - name: N15
      mass: 15.0001089
      abundance: 0.004
```
