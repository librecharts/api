import json
import os
from typing import Any, Optional
import psycopg
from psycopg_pool import AsyncConnectionPool
from helpers.classes import AnyChart
from helpers.exceptions import NoChartsForAirport
from helpers.factories import chart_factory

DATABASE_URL = os.environ.get('DATABASE_URL')

pool = AsyncConnectionPool(DATABASE_URL, open=False)


# Create decorators

def database_function(func):
    """
    Decorator to handle connection pooling
    """

    async def decorate(*args, **kwargs):
        connection = await pool.getconn()
        cursor = connection.cursor()
        value = await func(cursor, *args, **kwargs)
        await connection.commit()
        await cursor.close()
        await pool.putconn(connection)
        return value

    return decorate


@database_function
async def __initialize_database(cursor: psycopg.AsyncCursor) -> None:
    await cursor.execute("""CREATE TABLE IF NOT EXISTS charts(
                            title TEXT NOT NULL,
                            type TEXT NOT NULL,
                            filename TEXT NOT NULL UNIQUE,
                            filetype TEXT NOT NULL,
                            source JSON NOT NULL,
                            icao_code TEXT NOT NULL,
                            subtype TEXT,
                            runways TEXT[],
                            sids TEXT[],
                            stars TEXT[])""")


@database_function
async def insert_or_update_chart(cursor: psycopg.AsyncCursor, chart: AnyChart) -> None:
    """Duplicate-safe way of inserting and updating charts in the database if a chart exists it will be updated

    Parameters
    ----------
    cursor : psycopg.AsyncCursor
    chart : AnyChart

    Returns
    -------

    """

    def __clean_class_dump(dirty: AnyChart) -> dict[str, Any]:
        dump = dirty.model_dump()
        optional_keys = ['subtype', 'sids', 'stars', 'runways']
        for key in optional_keys:
            if key not in dump.keys():
                dump[key] = None
        dump['source'] = json.dumps(dump['source'])
        return dump

    clean_dump = __clean_class_dump(chart)

    await cursor.execute("SELECT COUNT(*) FROM charts WHERE filename=%s", (chart.filename,))
    count = (await cursor.fetchone())[0]
    if count == 1:  # Does the  chart already exist in the table?

        await cursor.execute("UPDATE charts SET title=%(title)s, type=%(type)s, filename=%(filename)s, filetype=%("
                             "filetype)s, source=%(source)s, icao_code=%(icao_code)s, subtype=%(subtype)s, "
                             "runways=%(runways)s, sids=%(sids)s, stars=%(stars)s WHERE filename=%(filename)s",
                             clean_dump)
    elif count > 1:  # Are there duplicates? If so remove and re-insert
        await cursor.execute("DELETE FROM charts WHERE filename=%s", (chart.filename,))
        await insert_or_update_chart(chart)
    else:  # If the chart doesn't exist, insert it
        await cursor.execute("INSERT INTO charts(title, type, filename, filetype, source, icao_code, subtype,"
                             "runways, sids, stars) VALUES (%(title)s, %(type)s, %(filename)s, %(filetype)s,"
                             " %(source)s, %(icao_code)s, %(subtype)s, %(runways)s, %(sids)s, %(stars)s)", clean_dump)


@database_function
async def get_charts_by_icao_code(cursor: psycopg.AsyncCursor, icao_code: str) -> list[AnyChart]:
    """Returns a list of charts per ICAO code

    Args:
        icao_code: The four letter ICAO code to search by

    Returns: list[AnyChart]
    Raises:
        NoChartsForAirport: When no charts are found for that ICAO code

    """
    await cursor.execute('SELECT * FROM charts WHERE icao_code=%s', (icao_code,))
    result_set = await cursor.fetchall()
    if not result_set:
        raise NoChartsForAirport(icao_code)

    return [chart_factory(data) for data in result_set]


@database_function
async def get_icao_codes(cursor: psycopg.AsyncCursor) -> set[str]:
    """Returns a unique list of ICAO codes registered in the system

    Returns: set[str]
    """
    await cursor.execute('SELECT icao_code FROM charts')
    return set([i[0] for i in await cursor.fetchall()])


@database_function
async def delete_charts_with_icao_code(cursor: psycopg.AsyncCursor, icao_code: str) -> None:
    """Deletes all charstfor a given ICAO code

    Args:
        icao_code: The four letter ICAO code to search by

    """
    await cursor.execute('DELETE FROM charts WHERE icao_code=%s', (icao_code,))
