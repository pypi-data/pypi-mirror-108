import logging
import re
import time
from collections import namedtuple
from typing import List, NamedTuple, Union

import requests

from ...client import Session
from ...models import Block, BlockFormat, BlockVersion
from .regex import INLINE_CITATION_BLOCK_REGEX

logger = logging.getLogger()

LocalReferenceItem = namedtuple(
    "LocalReferenceItem", ["block_path", "local_tag", "bibtex"]
)


class LocalMarkerItem(NamedTuple):
    remote_marker: str
    local_marker: str


def find_groups_in_content(regex_matcher: str, content: str):
    """
    Take a peice of tex content that we expect to contain one or more commands,
    find all instances based on the regex given and return the first groups

    Typically this is used to extract block_paths for different latex commands from
    TeX content
    """
    block_paths = []
    matches = re.finditer(regex_matcher, content)
    for match in matches:
        block_path = match[1]
        block_paths.append(block_path)

    return block_paths


def block_hash_to_url(
    api_url: str, block_hash: str, format: Union[BlockFormat, None] = None
):
    fmt = ""
    if format is not None:
        fmt = f"?format={format}"
    match = re.search(
        r"block:([A-Za-z0-9]{20})/([A-Za-z0-9]{20})/*([0-9]*)", block_hash
    )
    if match:
        if match[3]:
            return f"{api_url}/blocks/{match[1]}/{match[2]}/versions/{match[3]}{fmt}"
        return f"{api_url}/blocks/{match[1]}/{match[2]}{fmt}"
    raise ValueError(f"invalid block hash {block_hash}")


# TODO move to session - easier to mock
def get_model(session, url, model=BlockVersion):
    block = session._get_model(url, model)
    if not block:
        raise ValueError(f"Could not fetch the block {url}")
    return block


def fetch(url: str):
    resp = requests.get(url)
    if resp.status_code >= 400:
        raise ValueError(resp.content)
    return resp.content


def localize_references_from_content_block(
    session: Session, reference_list: List[LocalReferenceItem], content: str
):
    """Looks for cite TeX commands in the content then replaces the block ids
    with locally unique identifiers based on the local reference list.

    The reference list is extended as new references are found (side effect)

    Appends a unique hash to each new reference encountered
    """
    block_paths = find_groups_in_content(INLINE_CITATION_BLOCK_REGEX, content)
    patched_content = content

    for block_path in block_paths:
        # check for the reference in the reference list based on the block_path
        matched_references = [r for r in reference_list if r.block_path == block_path]
        existing_reference = (
            matched_references[0] if (len(matched_references) > 0) else None
        )

        if existing_reference is None:
            url = block_hash_to_url(session.api_url, block_path)
            logging.info(f"fetching reference block {url}")
            block = get_model(session, url, Block)
            logging.info("got reference block")

            # get latest version
            version_url = f"{url}/versions/{block.latest_version}?format=bibtex"
            logging.info(f"fetching reference version {version_url}")
            version = get_model(session, version_url)
            logging.info("got reference version")

            # update the list
            local_tag, plain_tag = parse_cite_tag_from_version(version.content)
            bibtex = version.content.replace(plain_tag, local_tag)

            reference_item = LocalReferenceItem(block_path, local_tag, bibtex)
            reference_list.append(reference_item)
            existing_reference = reference_item
            logging.info(f"using new reference {existing_reference.local_tag}")
        else:
            logging.info(f"using existing reference {existing_reference.local_tag}")

        # patch the content and move on
        patched_content = patched_content.replace(
            block_path, existing_reference.local_tag
        )

    return patched_content


def get_fast_hash():
    return hex(int(time.time_ns()))[2:]


def parse_cite_tag_from_version(content: str):
    tag = "ref"
    match = re.match("@article{([0-9a-zA-Z_]+),*\n", content)
    if match is not None:
        tag = match[1].replace(",", "")
    # adding quasi-random hash to save de-duping work
    hash_id = get_fast_hash()
    tag_with_hash = f"{tag}_{hash_id}"

    return tag_with_hash, tag
