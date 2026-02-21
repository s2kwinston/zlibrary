import asyncio

from curl_cffi.requests import AsyncSession

from .exception import LoopError
from .logger import logger
from typing import Dict, Optional, Tuple


# Impersonate Chrome 120 — replicates its TLS fingerprint to bypass bot detection
IMPERSONATE = "chrome120"

TIMEOUT = 180
HEAD_TIMEOUT = 4


async def GET_request(url, cookies=None, proxy_list=None) -> str:
    try:
        proxy = proxy_list[0] if proxy_list else None
        async with AsyncSession(impersonate=IMPERSONATE) as session:
            logger.info("GET %s" % url)
            resp = await session.get(
                url, cookies=cookies or {}, proxy=proxy, timeout=TIMEOUT
            )
            return resp.text
    except asyncio.CancelledError:
        raise LoopError("Asyncio loop has been closed before request could finish.")


async def GET_request_cookies(
    url, cookies=None, proxy_list=None
) -> Tuple[str, Dict[str, str]]:
    try:
        proxy = proxy_list[0] if proxy_list else None
        async with AsyncSession(impersonate=IMPERSONATE) as session:
            logger.info("GET %s" % url)
            resp = await session.get(
                url, cookies=cookies or {}, proxy=proxy, timeout=TIMEOUT
            )
            return (resp.text, dict(resp.cookies))
    except asyncio.CancelledError:
        raise LoopError("Asyncio loop has been closed before request could finish.")


async def POST_request(url, data, proxy_list=None) -> Tuple[str, Dict[str, str]]:
    try:
        proxy = proxy_list[0] if proxy_list else None
        async with AsyncSession(impersonate=IMPERSONATE) as session:
            logger.info("POST %s" % url)
            resp = await session.post(
                url, data=data, proxy=proxy, timeout=TIMEOUT
            )
            return (resp.text, dict(resp.cookies))
    except asyncio.CancelledError:
        raise LoopError("Asyncio loop has been closed before request could finish.")


async def HEAD_request(url, proxy_list=None):
    try:
        proxy = proxy_list[0] if proxy_list else None
        async with AsyncSession(impersonate=IMPERSONATE) as session:
            logger.info("Checking connectivity of %s..." % url)
            resp = await session.head(url, proxy=proxy, timeout=HEAD_TIMEOUT)
            return resp.status_code
    except Exception:
        return 0
