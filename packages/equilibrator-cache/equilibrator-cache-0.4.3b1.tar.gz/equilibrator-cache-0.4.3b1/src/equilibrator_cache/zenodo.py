"""Handles downloading an caching of files from Zenodo."""
# The MIT License (MIT)
#
# Copyright (c) 2013 The Weizmann Institute of Science.
# Copyright (c) 2018 Novo Nordisk Foundation Center for Biosustainability,
# Technical University of Denmark.
# Copyright (c) 2018 Institute for Molecular Systems Biology,
# ETH Zurich, Switzerland.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import asyncio
import hashlib
import logging
import pathlib
import warnings
from io import BytesIO
from json import JSONDecodeError
from typing import Dict, Optional

import appdirs
import httpx
import requests
from tenacity import RetryError, retry, stop_after_attempt
from tqdm.asyncio import tqdm


logger = logging.getLogger(__name__)


BASE_URL = "https://zenodo.org/api/"


def find_record_by_doi(doi: str, timeout: float = 5.0) -> Optional[dict]:
    """Find a Zenodo record by its DOI and return all the metadata.

    Parameters
    ----------
    doi : str
        The DOI of the requested entry
    timeout : float
        The request timeout (default: 5 seconds)

    Returns
    -------
    dict
        Containing all of the metadata.

    """
    params = {"q": f"doi:{doi.replace('/', '*')}"}

    for hit in requests.get(
        BASE_URL + "records", params=params, timeout=timeout
    ).json()["hits"]["hits"]:
        if hit["doi"] == doi:
            return hit
    raise ValueError(f"Cannot find a Zenodo record with doi = {doi}")


def download_from_url(url: str) -> BytesIO:
    """Download a file from a given URL using httpx.

    Parameters
    ----------
    url : str
        The URL address of the file.
    md5 : str, optional
        The MD5 checksum of the file, if given and the checksum doesn't match
        the downaloded file, an IOError is raised. The default is None.

    Returns
    -------
    BytesIO
        Containing the downloaded file.

    """
    data = BytesIO()
    client = httpx.Client()
    with client.stream("GET", url) as response:
        total = int(response.headers["Content-Length"])
        md5 = response.headers["content-md5"]

        num_bytes = 0
        with tqdm(
            total=total, unit_scale=True, unit_divisor=1024, unit="B"
        ) as progress:
            for chunk in response.iter_bytes():
                data.write(chunk)
                progress.update(len(chunk))
                num_bytes += len(chunk)
    client.close()

    if num_bytes < total:
        raise IOError(f"Failed to download file from {url}")

    data.seek(0)
    if hashlib.md5(data.read()).hexdigest() != md5:
        raise IOError(f"MD5 mismatch while trying to download file from {url}")

    data.seek(0)
    return data


@retry(stop=stop_after_attempt(3))
def get_zenodo_files(zenodo_doi: str) -> Dict[str, BytesIO]:
    """Download all files from a Zenodo entry synchronously."""
    data = find_record_by_doi(zenodo_doi)
    fnames = [d["key"] for d in data["files"]]
    urls = [d["links"]["self"] for d in data["files"]]
    data_streams = [download_from_url(url) for url in urls]
    return dict(zip(fnames, data_streams))


async def adownload_from_url(url: str) -> BytesIO:
    """Download a file from a given URL using httpx.

    Parameters
    ----------
    url : str
        The URL address of the file.
    md5 : str, optional
        The MD5 checksum of the file, if given and the checksum doesn't match
        the downaloded file, an IOError is raised. The default is None.

    Returns
    -------
    BytesIO
        Containing the downloaded file.

    """
    data = BytesIO()
    client = httpx.AsyncClient()
    async with client.stream("GET", url) as response:
        total = int(response.headers["Content-Length"])
        md5 = response.headers["content-md5"]

        num_bytes = 0
        with tqdm(
            total=total, unit_scale=True, unit_divisor=1024, unit="B"
        ) as progress:
            async for chunk in response.aiter_bytes():
                data.write(chunk)
                progress.update(len(chunk))
                num_bytes += len(chunk)
        await client.aclose()

    if num_bytes < total:
        raise IOError(f"Failed to download file from {url}")

    data.seek(0)
    if hashlib.md5(data.read()).hexdigest() != md5:
        raise IOError(f"MD5 mismatch while trying to download file from {url}")

    data.seek(0)
    return data


async def _aget_zenodo_files(zenodo_doi: str) -> Dict[str, BytesIO]:
    """Run the aget_zenodo_files coroutine asynchronously."""
    data = find_record_by_doi(zenodo_doi)
    fnames = [d["key"] for d in data["files"]]
    urls = [d["links"]["self"] for d in data["files"]]
    tasks = [adownload_from_url(url) for url in urls]
    data_streams = await asyncio.gather(*tasks)
    return dict(zip(fnames, data_streams))


@retry(stop=stop_after_attempt(3))
def aget_zenodo_files(zenodo_doi: str) -> Dict[str, BytesIO]:
    """Download all the files stored in Zenodo (under a specific DOI).

    Parameters
    ----------
    zenodo_doi : str
        the DOI of the Zenodo entry.

    Returns
    -------
    Dict
        the dictionary with file names as keys, and the file contents as
        values.

    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(_aget_zenodo_files(zenodo_doi))


def get_zenodo_checksum(zenodo_doi: str, zenodo_fname: str) -> Optional[str]:
    """Download all the files stored in Zenodo (under a specific DOI).

    Parameters
    ----------
    zenodo_doi : str
        the DOI of the Zenodo entry.

    Returns
    -------
    str
        latest version of the Zenodo entry.

    """
    try:
        data = find_record_by_doi(zenodo_doi, timeout=1.0)
    except requests.exceptions.ConnectionError:
        warnings.warn("No connection to Zenodo, cannot verify local version.")
        return None
    except requests.exceptions.Timeout:
        warnings.warn(
            "Connection to Zenodo timed out, cannot verify local version."
        )
        return None
    except JSONDecodeError:
        warnings.warn(
            "JSON file from Zenodo is corrupted, cannot verify local version."
        )
        return None

    for d in data["files"]:
        if d["key"] == zenodo_fname:
            fmt, checksum = d["checksum"].split(":", 1)
            assert fmt == "md5", "Checksum format must be MD5"
            return checksum

    raise KeyError(
        f"The file {zenodo_fname} was not found in the Zenodo entry: "
        f"{zenodo_doi}"
    )


def get_cached_filepath(zenodo_doi: str, zenodo_fname: str) -> pathlib.Path:
    """Get data from a file stored in Zenodo (or from cache, if available).

    Parameters
    ----------
    zenodo_doi : str
        the DOI of the Zenodo entry.
    zenodo_fname : str
        the specific filename to fetch from Zenodo.

    Returns
    -------
    str
        the path to the locally cached file.

    """

    cache_directory = pathlib.Path(
        appdirs.user_cache_dir(appname="equilibrator")
    )
    cache_directory.mkdir(parents=True, exist_ok=True)

    cache_fname = cache_directory / zenodo_fname

    if cache_fname.exists():
        # make sure that it is in the correction version and not corrupted.

        logging.info("Fetching metadata about the Compound Cache from Zenodo")
        md5 = get_zenodo_checksum(zenodo_doi, zenodo_fname)
        if md5 is None:
            # we cannot perform the checksum test, so we assume that everything
            # is okay.
            return cache_fname

        # verify that the checksum from Zenodo matches the cached file.
        logging.info("Validate the cached copy using MD5 checksum")
        with cache_fname.open("rb") as fp:
            if md5 == hashlib.md5(fp.read()).hexdigest():
                return cache_fname

        # if the checksum is not okay, it means the file is corrupted or
        # exists in an older version. therefore, we ignore it and override
        # it with a newly downloaded version

    logging.info("Fetching a new version of the Compound Cache from Zenodo")
    try:
        try:
            # try downloading the files from Zenodo asynchronously
            dataframe_dict = aget_zenodo_files(zenodo_doi)
        except RetryError:
            # try again this time synchronously
            dataframe_dict = get_zenodo_files(zenodo_doi)
    except JSONDecodeError:
        raise IOError(
            "Some required data needs to be downloaded from Zenodo.org, but "
            "there is a communication problem at the "
            "moment. Please wait and try again later."
        )

    cache_fname.write_bytes(dataframe_dict[zenodo_fname].getbuffer())

    return cache_fname
