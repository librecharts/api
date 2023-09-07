ICAO_CODE_CONSTRAINTS = {
    'min_length': 4,
    'max_length': 4,
    'pattern': r'[a-zA-Z]{4}',
    'examples': ['LPPT', 'eddm']
}

CHARTS_INFORMATION = {
    "name": "Get Charts",
    "description": "Returns an array of all Chart objects associated with a given ICAO code",
    "response_description": "Array of Chart objects",
    "tags": ["Charts"]
}

CATEGORIZED_CHARTS_INFORMATION = {
    "name": "Get Categorized Charts",
    "description": "Returns an array of all Chart objects associated with a given ICAO code",
    "response_description": "Array of Chart objects",
    "tags": ["Charts"]

}

CODES_INFORMATION = {
    "name": "Get ICAO codes",
    "description": "Returns an array of all ICAO codes with charts in the system",
    "tags": ["Information"]
}

COVERAGE_INFORMATION = {
    "name": "Get Coverage",
    "description": "Returns a CoverageStatistics for a given provider",
    "tags": ["Internal"]
}

UPDATE_INFORMATION = {
    "name": "Update ",
    "description": "Returns a CoverageStatistics for a given provider",
    "tags": ["Internal"]
}