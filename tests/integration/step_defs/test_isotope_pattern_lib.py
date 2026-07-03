from os import path
from typing import List

import pytest
import yaml
from pytest_bdd import (
    given,
    parsers,
    scenario,
    then
)

from isotope_pattern_lib import api
from isotope_pattern_lib.types.types import IsotopeFormula


@scenario(
    path.join('..', 'features', 'isotope_pattern_lib.feature'),
    "Should return correct pattern when settings are default and molecular formula is provided",
)
def test__should_return_correct_pattern__when_settings_are_default_and_formula_is_provided():
    # No need to have anything here
    pass


@scenario(
    path.join('..', 'features', 'isotope_pattern_lib.feature'),
    "Should return correct pattern when settings are customized and molecular formula is provided",
)
def test__should_return_correct_pattern__when_settings_are_customized_and_formula_is_provided():
    # No need to have anything here
    pass


@given(parsers.parse('Molecular "{formula}" as a raw string'), target_fixture='molecular_formula')
def molecular_formula(formula: str) -> str:

    return formula


@given('Different settings are provided')
def settings():

    api.set_parser(path.join('tests', 'data', 'integration', 'config.yaml'))


@given('The pattern computation is triggered', target_fixture='pattern')
def pattern(molecular_formula: str) -> List[IsotopeFormula]:

    return api.compute_isotope_pattern(formula_string=molecular_formula)


@then(parsers.parse('The resulting pattern corresponds to the one in "{file}"'))
def assert_pattern_equality(pattern: List[IsotopeFormula], file: str):

    with open(path.join('tests', 'data', 'integration', file), 'r') as file:
        expected_pattern = yaml.safe_load(file)

    assert len(pattern) == len(expected_pattern['isotope_formulas'])

    for formula, expected_formula in zip(pattern, expected_pattern['isotope_formulas']):
        assert formula.name == expected_formula['name']
        assert formula.mass == pytest.approx(expected=expected_formula['mass'], abs=0.001)
        assert formula.probability == pytest.approx(expected=expected_formula['probability'], abs=0.001)
