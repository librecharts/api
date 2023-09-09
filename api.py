import os
from functools import lru_cache
from typing import Annotated, Optional
from starlette.middleware.cors import CORSMiddleware

import config
from helpers.classes import AnyChart, CoverageStatistics, Manifest
from helpers.coverage import get_vatsim_statistics, get_stp_statistics, get_poscon_statistics
from helpers.database import pool, __initialize_database, get_charts_by_icao_code, get_icao_codes, \
    insert_or_update_chart, delete_charts_with_icao_code
from fastapi import FastAPI, Path, HTTPException, Header, Depends
from helpers.docs import CHARTS_INFORMATION, ICAO_CODE_CONSTRAINTS, CATEGORIZED_CHARTS_INFORMATION, CODES_INFORMATION, \
    COVERAGE_INFORMATION
import sentry_sdk

api = FastAPI(
    redoc_url='/',
    docs_url=None
)

api.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Token"],
)

sentry_sdk.init(
    dsn=os.getenv('SENTRY_URI'),
    traces_sample_rate=1.0,
    profiles_sample_rate=0.1,
)


@lru_cache()
def get_settings():
    return config.Settings()


@api.get("/charts/{code}", **CHARTS_INFORMATION)
async def charts_by_code(code: Annotated[str, Path(title="The ICAO code of the airport", **ICAO_CODE_CONSTRAINTS)]) \
        -> list[AnyChart]:
    code = code.upper()
    return await get_charts_by_icao_code(code)


@api.get("/charts/{code}/categorized", **CATEGORIZED_CHARTS_INFORMATION)
async def categorized_charts_per_code(
        code: Annotated[str, Path(title="The ICAO code of the airport", **ICAO_CODE_CONSTRAINTS)]) \
        -> dict[str, list[AnyChart]]:
    code = code.upper()
    charts = await get_charts_by_icao_code(code)

    # @NOTE(Mauro): There are more "pythonic" and code golfy style ways of doing this but this is O(n) whereas most of
    #               those are O(n^2) or require iterating twice

    d: dict[str, list[AnyChart]] = {}

    for chart in charts:
        if chart.type in d.keys():
            d[chart.type] += [chart]
        else:
            d[chart.type] = [chart]

    return d


@api.post("/update")
async def update_charts(manifest: Manifest, settings: Annotated[config.Settings, Depends(get_settings)],
                        token: Annotated[str | None, Header()] = None) -> Optional[dict[str, set[str]]]:
    if token:
        if token == settings.update_token:
            icao_codes = set([chart.icao_code for chart in manifest.charts])
            system_icao_codes = await get_icao_codes()
            for code in system_icao_codes.intersection(icao_codes):
                await delete_charts_with_icao_code(code)
            for chart in manifest.charts:
                await insert_or_update_chart(chart)
            return {'codes': icao_codes}
    raise HTTPException(401)


@api.get('/codes', **CODES_INFORMATION)
async def codes() -> set[str]:
    return await get_icao_codes()


@api.get('/coverage/{provider}', **COVERAGE_INFORMATION)
async def coverage(provider: str) -> CoverageStatistics:
    match provider.lower():
        case "poscon":
            return get_poscon_statistics()
        case "vatsim":
            return get_vatsim_statistics()
        case "stp":
            return get_stp_statistics()


@api.on_event("startup")
async def open_pool():
    await pool.open()
    await __initialize_database()


@api.on_event("shutdown")
async def close_pool():
    await pool.close()
