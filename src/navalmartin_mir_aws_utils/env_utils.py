import os
from typing import List


def get_or_raise_environment_vars(var_names: List[str]) -> dict:
    """Loops over the given variable names and checks the environment
    about its value. If the value is None it raises an exception

    Parameters
    ----------
    var_names: The variable names to look for

    Returns
    -------

    A dictionary with the values of the environment variables
    """

    variables = {}

    for name in var_names:

        if name in variables:
            raise ValueError(f'Duplicate variable {name} found')
        value = os.getenv(name, default=None)

        if value is None:
            raise ValueError(f"Environment variable {name} is not set")

        variables[name] = value

    return variables
