# CC BY-NC-ND 4.0 2023 Mauro M. - factories in project api

# The aforementioned code and documents are protected and released to the public under the Creative Commons
# Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) License which can be viewed in license.md or on the
# Creative Commons website (https://creativecommons.org/licenses/by-nc/4.0/). Any failure to comply with the terms
# designated in the license will be met with swift judicial action by the author.

# By downloading, executing or otherwise transferring the contents of this repository by any means you are legally
# bound to the terms stipulated in the license.

from typing import Union

from helpers import (
    Chart,
    AirspaceChart,
    ILSChart,
    DepartureChart,
    ApproachChart,
    ArrivalChart, AirportChart,
)


def chart_factory(
    content: dict[str, Union[str, bool]]
) -> Union[Chart, AirspaceChart, ApproachChart, ILSChart, DepartureChart, ArrivalChart, AirportChart]:
    """
    Takes a properly formatted chart manifest and converts it to the proper python object

    Parameters
    ----------
    content: dict
        Chart information from the manifest
    """

    match content["type"]:
        case "approach":

            def __check_ils_approach(subtype: Union[str, list[str]]) -> bool:
                if isinstance(subtype, list):
                    return "ils" in [i.lower() for i in subtype]
                else:
                    return subtype.lower() == "ils"

            if __check_ils_approach(content["subtype"]):
                return ILSChart(**content)

            else:
                return ApproachChart(**content)

        case "departure":

            return DepartureChart(**content)

        case "arrival":

            return ArrivalChart(**content)

        case "airspace":

            return AirspaceChart(**content)

        case "visual":

            return AirportChart(**content)