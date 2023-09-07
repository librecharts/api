# CC BY-NC-ND 4.0 2023 Mauro M. - helpers in project api
from enum import StrEnum
# The aforementioned code and documents are protected and released to the public under the Creative Commons
# Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) License which can be viewed in license.md or on the
# Creative Commons website (https://creativecommons.org/licenses/by-nc/4.0/). Any failure to comply with the terms
# designated in the license will be met with swift judicial action by the author.

# By downloading, executing or otherwise transferring the contents of this repository by any means you are legally
# bound to the terms stipulated in the license.

from typing import Union, Optional
from pydantic import BaseModel


class Source(BaseModel):
    """
    Represents a Source for a given chart

    Attributes:
        name (str): Human-readable source name usually the authority that publishes the charts
        url (str): URL for the given source
        contributor (str): GitHub profile name for the contributor
        cached (bool): If LibreCharts caches the charts, or they're served directly

    """

    name: str
    url: str
    contributor: str
    cached: bool = True


class Chart(BaseModel):
    """
    Represents a basic chart associated with a given airport

    Attributes:
        title (str): The chart's title
        type (str): Represents the type of the chart
        filename (str): Filename of the chart file
        filetype (str): Mime-type of the chart file (will usually be application/pdf)
        icao_code (str): ICAO code of the airport the chart reffers to
    """
    title: str
    type: str
    filename: str
    filetype: str
    source: Source
    icao_code: str


class GroundChart(Chart):
    """
    Represents a generic ground chart for a given airport, this includes parking and taxiing

    Attributes:
        subtype (str): Optional subtype of the chart
    """

    subtype: Optional[str] = None


class RunwayChart(Chart):
    """
    Represents a generic chart for a given runway
    Attributes:
        runways (list[str]): Runway or runway(s) the chart is associated with, can be ['*'] for all runways
    """

    runways: Optional[list[str]] = None


class ApproachChart(RunwayChart):
    """
    Represents an approach chart for a given runway

     Attributes:
        subtype (str): Optional subtype of the chart
    """

    subtype: Optional[str] = None


class DepartureChart(RunwayChart):
    """
    Represents a departure chart for a given runway

     Attributes:
        subtype (str): Optional subtype of the departure chart
        sids (list[str]): SIDs in this departure chart
    """

    subtype: Optional[Union[str, list[str]]] = None
    sids: Optional[list[str]] = None


class ArrivalChart(RunwayChart):
    """
    Represents an arrival chart for a given runway

    Attributes:
        subtype (str): Optional subtype of the arrival chart
        sids (list[str]): STARs in this arrival chart
    """

    subtype: Optional[Union[str, list[str]]] = None
    stars: Optional[list[str]] = None


class Providers(StrEnum):
    poscon = 'poscon'
    stp = 'stp'
    vatsim = 'vatsim'


class CoverageStatistics(BaseModel):
    """
    Represents a coverage object for a given provider


    Attributes:

    """
    provider: Providers
    departure_airports: Optional[list[str]]
    arrival_airports: Optional[list[str]]
    alternate_airports: Optional[list[str]]


# Typing

AnyChart = Union[Chart, ApproachChart, DepartureChart, ArrivalChart, GroundChart]


class Manifest(BaseModel):
    charts: list[AnyChart]