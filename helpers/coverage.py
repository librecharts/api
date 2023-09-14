import random
from typing import Optional, Any

from fastapi import requests, HTTPException
import requests
from helpers.classes import CoverageStatistics

VATSIM_STATUS_URL = 'https://status.vatsim.net/status.json'
POSCON_DATA_ENDPOINT = 'https://hqapi.poscon.net/online.json'
STP_DATA_ENDPOINT = 'https://simtoolkitpro.co.uk/api/flights.stkp'


def __clean_array(a: list[str]) -> list[str]:
    """De-duplicates, ensures no empty values and that all array values have the length of 4

    :param a: Array to clean
    :return: Array with no duplicates and empty values
    """
    return list(set([i for i in a if i and len(i) == 4]))


def __get_vatsim_data_url() -> Optional[str]:
    """Returns a valid random VATSIM data url

    :return: a valid VATSIM data URL
    """

    # @NOTE(Mauro): This is recommended practice as per the VATSIM developer information
    # ref: https://github.com/vatsimnetwork/developer-info/wiki/Data-Feeds

    response = requests.get(VATSIM_STATUS_URL)

    if response.status_code != 200:
        raise HTTPException(detail="Upstream failure fetching VATSIM data url", status_code=response.status_code)

    return random.choice(response.json()['data']['v3'])


def get_vatsim_statistics() -> Optional[CoverageStatistics]:
    """Returns a valid statistics dict from VATSIM

    :return: A dict containing arrival, departure and alternate airport arrays
    """

    response = requests.get(__get_vatsim_data_url())

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failure fetching VATSIM data JSON")

    json = response.json()

    departure_airports: list[str] = []
    arrival_airports: list[str] = []
    alternate_airports: list[str] = []

    for pilot in json['pilots']:
        pilot: dict[str, Any]
        if 'flight_plan' in pilot.keys():
            flight_plan = pilot['flight_plan']

            if flight_plan:  # In certain cases flight_plan can be null
                departure_airports.append(flight_plan['departure'])
                arrival_airports.append(flight_plan['arrival'])
                if flight_plan['alternate'] != 'NONE':  # Some pilots file without an alternate
                    alternate_airports.append(flight_plan['alternate'])

    return CoverageStatistics(**{
        "provider": "vatsim",
        "departure_airports": __clean_array(departure_airports),
        "arrival_airports": __clean_array(arrival_airports),
        "alternate_airports": __clean_array(alternate_airports)
    })


def get_poscon_statistics() -> Optional[CoverageStatistics]:
    """Returns a valid statistics dict from POSCON

    :return: A dict containing arrival, departure and alternate airport arrays
    """

    response = requests.get(POSCON_DATA_ENDPOINT)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failure fetching POSCON data JSON")

    json = response.json()

    departure_airports: list[str] = []
    arrival_airports: list[str] = []
    alternate_airports: list[str] = []

    for flight in json['flights']:
        flight: dict[str, Any]
        if 'flightplan' in flight.keys():
            flight_plan = flight['flightplan']

            if flight_plan:  # In certain cases flight_plan can be null
                departure_airports.append(flight_plan['dep'])
                arrival_airports.append(flight_plan['dest'])
                if flight_plan['altnt']:
                    alternate_airports.append(flight_plan['altnt'])
                if flight_plan['altnt2']:
                    alternate_airports.append(flight_plan['altnt2'])

    return CoverageStatistics(**{
        "provider": "poscon",
        "departure_airports": __clean_array(departure_airports),
        "arrival_airports": __clean_array(arrival_airports),
        "alternate_airports": __clean_array(alternate_airports)
    })


def get_stp_statistics() -> Optional[CoverageStatistics]:
    """Returns a valid statistics dict from SimToolkitPro

    :return: A dict containing arrival, departure and alternate airport arrays
    """

    response = requests.get(STP_DATA_ENDPOINT)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failure fetching SimToolKitPro data JSON")

    json: dict[str, list] = response.json()

    departure_airports: list[str] = []
    arrival_airports: list[str] = []
    alternate_airports: list[str] = []

    for flight in json.values():
        if flight[7] != '-':
            departure_airports.append(flight[7])
        if flight[8] != '-':
            arrival_airports.append(flight[8])

    return CoverageStatistics(**{
        "provider": "stp",
        "departure_airports": __clean_array(departure_airports),
        "arrival_airports": __clean_array(arrival_airports),
        "alternate_airports": __clean_array(alternate_airports)
    })