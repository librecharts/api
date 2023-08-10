# CC BY-NC-ND 4.0 2023 Mauro M. - helpers in project api

# The aforementioned code and documents are protected and released to the public under the Creative Commons
# Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) License which can be viewed in license.md or on the
# Creative Commons website (https://creativecommons.org/licenses/by-nc/4.0/). Any failure to comply with the terms
# designated in the license will be met with swift judicial action by the author.

# By downloading, executing or otherwise transferring the contents of this repository by any means you are legally
# bound to the terms stipulated in the license.

from dataclasses import dataclass
from typing import Union, Optional


@dataclass
class Source:
    """
    Represents a Source for a given chart

    Parameters
    ----------

    name: str
        Human-readable source name
    url: str
        URL for the given source
    contributor: str
        Github profile name for the contributor
    cached: bool
        If LibreCharts caches the charts, or they're served directly

    """

    name: str
    url: str
    contributor: str
    cached: bool = True


@dataclass
class Chart:
    """
    Represents a generic chart

    Parameters
    ----------

    chart_type: str
        Represents the type of the chart, this will point to a subclass in the factory
    filename: str
        Filename of the chart file
    filetype: str
        Mime-type of the chart file (will usually be application/pdf)
    """

    chart_type: str
    filename: str
    filetype: str
    __raw_source: dict[str, Union[str, bool]]

    @property
    def source(self) -> Optional[Source]:
        """
        Returns the source object for the given chart

        Returns
        -------
        Source

        """
        try:
            return Source(**self.__raw_source)
        except TypeError:
            return None


@dataclass
class AirspaceChart(Chart):
    """
    Represents a chart for a given FIR

    Parameters
    ----------

    fir: str
        The FIR the chart is included in
    """

    fir: str
    subtype: str


@dataclass
class AirportChart(Chart):
    """
    Represents a generic chart for a given airport

    Parameters
    ----------

    icao_code: str
        ICAO code of the airport this chart is associated with
    """

    icao_code: str


@dataclass
class GroundChart(AirportChart):
    """
    Represents a generic ground chart for a given airport, this includes parking
    and taxiing

    Parameters
    ----------

    subtype: str
        Optional subtype of the chart
    """

    subtype: Optional[str]


@dataclass
class RunwayChart(AirportChart):
    """
    Represents a generic chart for a given runway

    Parameters
    ----------

    runway: str
       Runway or runway(s) the chart is associated with
    """

    runway: Union[str, list[str]]


@dataclass
class ApproachChart(RunwayChart):
    """
    Represents an approach chart for a given runway


    """

    subtype: Union[str, list[str]]


@dataclass
class ILSChart(ApproachChart):
    """
    Represents an ILS approach chart for a given runway.
    This is a breakout given the particularities of an ILS approach


    """

    categories: list[str] = None


@dataclass
class DepartureChart(RunwayChart):
    """
    Represents a departure chart for a given runway


    """

    subtype: Union[str, list[str]] = None
    stars: list[str] = None


@dataclass
class ArrivalChart(RunwayChart):
    """
    Represents a departure chart for a given runway


    """

    subtype: Union[str, list[str]] = None
    sids: list[str] = None
