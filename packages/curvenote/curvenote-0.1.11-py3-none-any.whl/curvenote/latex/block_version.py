import logging
from typing import List, Optional, Union

from curvenote.latex import utils

from ..client import Session
from ..models import (
    BlockKind,
    BlockVersion,
)
from . import utils

logger = logging.getLogger()

LANG = "___LANG___"
CODE_CONTENT = "___CODE_CONTENT___"

CODE_BLOCK_TPL = rf"""\begin{{minted}}[tabsize=4, linenos, mathescape, numbersep=5pt, framesep=2mm]{{{LANG}}}
{CODE_CONTENT}
\end{{minted}}
"""


class LatexBlockVersion:
    """
    Class to represent an block in the latex project.
    Encapulates operations applied in processing a block's content including
    calls to fetch content that it encapsulates
    """

    def __init__(self, session: Session, version: BlockVersion):
        self.session = session
        self.version = version
        self._content = ""

    @property
    def content(self):
        return self._content

    def localize(self, assets_folder: str, reference_list: List[str]):
        content = ""
        kind = self.version.kind
        if kind == BlockKind.content:
            logger.info("Found: Content Block")
            try:
                content = utils.localize_images_from_content_block(
                    self.session, assets_folder, self.version.content
                )
            except ValueError as err:
                logging.error(
                    f"Caught error trying to localize images for block {str(self.version.id)}, skipping"
                )
                logging.error(err)
            try:
                content = utils.localize_references_from_content_block(
                    self.session, reference_list, content
                )
            except ValueError as err:
                logging.error(
                    "Caught error trying to localize references for block %s, skipping",
                    str(self.version.id),
                )
                logging.error(err)
        elif kind == BlockKind.output:
            logger.info(
                "Found: Output Block - num outputs: %s", len(self.version.outputs)
            )
            content = utils.localize_images_from_output_block(
                assets_folder, self.version
            )
        elif kind == BlockKind.code:
            logger.info("Found: Code Block - wrapping content in minted")
            content = CODE_BLOCK_TPL.replace(
                LANG, "python").replace(CODE_CONTENT, self.version.content)
        elif kind == BlockKind.image:
            logger.info("Found: Top Level Image Block")
            try:
                content = utils.localize_image_from_top_level_block(
                    self.session, assets_folder, self.version
                )
            except ValueError as err:
                logging.error(
                    "Caught error trying to localize top level image %s, skipping",
                    str(self.version.id),
                )
                logging.error(err)
        else:
            logger.warning("Can't process block with kind: %s yet", kind)
            raise ValueError(f"Unknown block kind {kind}")
        self._content = content
