import pydantic
from typing import Optional, List, Union

from qcware.types.optimization.utils import intlist_to_binlist

from . import utils
from qcware.types.optimization import Domain


class BruteOptimizeResult(pydantic.BaseModel):
    """Return type for brute force maximization and minimization.

    When solution_exists == False, we must have value is None and
    arguments == [].

    Arguments are specified with a list of strings that describe solutions.
    For the boolean case, this means something like ['00101', '11100'] and
    for the spin case, this means something like ['++-+-', '---++'].
    """
    domain: Domain
    value: Optional[int] = None
    arguments: List[str] = []
    solution_exists: bool = True

    @pydantic.validator('solution_exists', always=True)
    def no_solution_check(cls, sol_exists, values):
        if not sol_exists:
            if not values['value'] is None:
                raise ValueError('Value given but solution_exists=False.')
            if not values['arguments'] == []:
                raise ValueError('arguments given but solution_exists=False.')

        else:
            if values['value'] is None or values['arguments'] == []:
                raise ValueError(
                    'solution_exists=True, but no solution was specified.')
        return sol_exists

    def int_argument(self) -> List[List[int]]:
        """Convert arguments to a list of list of ints."""
        def to_int(x: str):
            if self.domain is Domain.BOOLEAN:
                return int(x)
            else:
                if x == '+':
                    return 1
                elif x == '-':
                    return -1
                else:
                    raise ValueError(
                        f'Unrecognized symbol {x}. Expected \'+\' or \'-\'.')

        return [[to_int(x) for x in s] for s in self.arguments]

    @property
    def num_variables(self):
        if not self.solution_exists:
            return
        return len(self.arguments[0])

    def __repr__(self):
        if self.solution_exists:
            out = 'forge.return_types.BruteOptimizeResult(\n'
            out += f'value={self.value}\n'
            char_estimate = self.num_variables * len(self.arguments)
            out += utils.short_list_str(self.arguments, char_estimate,
                                        'arguments')
            return out + '\n)'
        else:
            return (
                'forge.return_types.BruteOptimizeResult(solution_exists=False)'
            )
