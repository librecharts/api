from fastapi import HTTPException


class NoChartsForAirport(HTTPException):
    """
    Raised when a given ICAO code doesn't have any charts in the system
    """
    def __init__(self, icao_code: str):
        self.icao_code = icao_code
        self.status_code = 404
        self.detail = f'No charts found for ICAO code {icao_code}'
