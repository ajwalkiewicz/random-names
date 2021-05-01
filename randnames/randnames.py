"""Main module for randnames

>>> import randomnames
>>> randomnames.full_name()
'John Doe'
"""

import random
import json
import os
import warnings
from bisect import bisect_left

_THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
_COUNTRIES_BASE = os.listdir(os.path.join(_THIS_FOLDER, "data"))

# LAST_NAMES_PATH = os.path.join(_THIS_FOLDER, "data", "US", "last_names")
FIRST_NAMES_PATH = os.path.join(_THIS_FOLDER, "data", "US", "first_names")

_available_sex = ("M", "F", "N")

class InvalidSexArgument(Exception):
    def __init__(self, sex: str):
        self.sex = sex
        self.message = f"{self.sex} not in {_available_sex}"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.sex} -> {self.message}"


def _draw_name(
    name,
    year: int = None,
    sex: str = None,
    country: str = None,
    weights: bool = True
    ) -> str:
    
    if not country:
        country = random.choice(_COUNTRIES_BASE)

    database_files = os.listdir(os.path.join(_THIS_FOLDER, "data", country, name))
    database_years = set(year.split("_")[0] for year in database_files)
    data_range = (int(min(database_years)), int(max(database_years)))

    if not year:
        year = random.randint(*data_range)

    if not min(data_range) <= year <= max(data_range):
        message = f"{year} -> {year} not in range {data_range}"
        warnings.warn(message) 

    info = os.path.join(_THIS_FOLDER, "data", country, "info.json")
    with open(info, "r") as info:
        available_sex = json.load(info)[name]

    if sex is None:
        sex = random.choice(available_sex)

    if str(sex).capitalize() not in available_sex:
        raise InvalidSexArgument(sex)

    # Correction of year index. If bisect_left returns int > len(data_range) return bisect_left -1
    year_index = lambda d, y: bisect_left(d, y) if bisect_left(d, y) != len(d) else bisect_left(d, y) - 1

    year = data_range[year_index(data_range, year)]
    data_set_name = f'{year}_{sex}'
    data_set_path = os.path.join(_THIS_FOLDER, "data", country, name, data_set_name)

    with open(data_set_path) as json_file:
        data_set = json.load(json_file)
        name_population = data_set["Names"]
        name_weights = data_set["Totals"]
        if weights:
            last_name = random.choices(name_population, cum_weights=name_weights)[0]
        else:
            last_name = random.choices(name_population)[0]
    return last_name

# Main functions

def last_name(year: int = None, sex: str = None, country: str = None, weights: bool = True) -> str:
    """Return random last name

    :param year: year of source database, defaults to None
    :type year: int, optional
    :param country: select database country, defaults to False
    :type country: str, optional
    :raises YearNotInRange: throw error if year is not in valid range
    :return: last name as string
    :rtype: str

    >>> last_name()
    'Doe'
    """
    last_name = _draw_name("last_names", year=year, sex=sex, country=country, weights=weights)
    return last_name

def first_name(year: int = None, sex: str = None, country: str = None, weights: bool = True) -> str:
    """Return random first name

    :param year: year of source database, defaults to None
    :type year: int, optional
    :param sex: first name gender, defaults to None
    :type sex: str, optional
    :raises YearNotInRange: If year is not in valid range
    :raises InvalidSexArgument: If invalid sex argument
    :return: first name as string
    :rtype: str

    >>> first_name()
    'John'
    """
    first_name = _draw_name("first_names", year=year, sex=sex, country=country, weights=weights)
    return first_name

# Flavor functions

def full_name(year: int = None, sex: str = None) -> str:
    """Return random first and las name 

    :param year: year of source database, defaults to None
    :type year: int, optional
    :param sex: first name gender, defaults to None
    :type sex: str, optional
    :return: full name as string
    :rtype: str

    >>> full_name()
    'John Doe'
    """
    return f"{first_name(year, sex)} {last_name(year)}"

# Support functions

def available_countries() -> list:
    """Return list of available countries

    :return: lis of available countries
    :rtype: list
    """
    return os.listdir(os.path.join(_THIS_FOLDER, "data"))

if __name__ == "__main__":
    # last_name()
    _draw_name("first_names", sex="M", country="US")