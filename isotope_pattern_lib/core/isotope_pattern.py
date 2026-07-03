import itertools
from typing import List, Any, Generator

from scipy.stats import multinomial

from isotope_pattern_lib.types.types import (
    Isotope,
    IsotopeFormula,
    MolecularFormula
)
from isotope_pattern_lib.utils import utils


def compute_isotope_pattern(formula: MolecularFormula) -> Generator[IsotopeFormula, Any, None]:

    element_isotope_formulas = {}
    for element, count in formula.elements.items():
        element_isotope_formulas[element] = compute_isotope_distributions(element.isotopes, count)

    for combination in itertools.product(*element_isotope_formulas.values()):

        name = ""
        counts = {}
        probability = 1.0
        for isotope_formula in combination:
            name += isotope_formula.name
            counts.update(isotope_formula.isotopes)
            probability *= isotope_formula.probability

        yield IsotopeFormula(
            name=name,
            isotopes=counts,
            probability=probability,
        )


def compute_isotope_distributions(isotopes: List[Isotope], element_count: int) -> List[IsotopeFormula]:

    distribution = multinomial(n=element_count, p=[isotope.abundance for isotope in isotopes])

    isotope_formulas = []
    for array in utils.generate_arrays_with_preserved_sum(total_sum=element_count, size=len(isotopes)):
        probability = distribution.pmf(array)
        isotope_counts = dict(zip(isotopes, array))
        isotope_formulas.append(IsotopeFormula(
            name="".join([f"{isotope.name}[{count}]" for isotope, count in isotope_counts.items()]),
            isotopes=isotope_counts,
            probability=probability
        ))

    return isotope_formulas
