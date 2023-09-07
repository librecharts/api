# CC BY-NC-ND 4.0 2023 Mauro M. - factories in project api

# The aforementioned code and documents are protected and released to the public under the Creative Commons
# Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) License which can be viewed in license.md or on the
# Creative Commons website (https://creativecommons.org/licenses/by-nc/4.0/). Any failure to comply with the terms
# designated in the license will be met with swift judicial action by the author.

# By downloading, executing or otherwise transferring the contents of this repository by any means you are legally
# bound to the terms stipulated in the license.

from typing import Union, Any

from helpers.classes import (
    Chart,
    DepartureChart,
    ApproachChart,
    ArrivalChart,
    GroundChart,
)


def __create_kwargs(tuple_: tuple[Union[str, dict[str, str], list[str]]]) -> dict[str, Any]:
    keys = ['title', 'type', 'filename', 'filetype', 'source', 'icao_code', 'subtype', 'runways', 'sids', 'stars']
    assert len(keys) == len(tuple_)
    return {key: value for key, value in zip(keys, tuple_)}


def chart_factory(
        content: Union[dict[str, Union[str, bool, list[str], dict[str]]], tuple[Union[str, dict[str, str], list[str]]]]
) -> Union[Chart, ApproachChart, DepartureChart, ArrivalChart]:
    """
    Takes a properly formatted chart manifest and converts it to the proper python object

    Parameters
    ----------
    content: dict
        Chart information from the manifest
    """

    if isinstance(content, tuple):
        content = __create_kwargs(content)

    match content["type"]:

        case "approach":
            return ApproachChart(**content)

        case "departure":

            return DepartureChart(**content)

        case "arrival":

            return ArrivalChart(**content)

        case "ground":

            return GroundChart(**content)

        case _:

            return Chart(**content)
