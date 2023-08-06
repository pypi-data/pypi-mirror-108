from .get_image_block import get_image_block
from ...models import BlockVersion, BlockChildID
from ...client import Session
from .index import get_fast_hash
import logging

VERSION_ID = "___VERSION_ID___"
CAPTION = "___CAPTION___"
LABEL = "___LABEL___"

IMAGE_LATEX_TPL = rf"""\begin{{figure}}[h]
  \centering
  \includegraphics[width=0.4\linewidth]{{{VERSION_ID}}}
  \caption{{{CAPTION}}}
  \label{{{LABEL}}}
\end{{figure}}
"""


def version_id_to_block_path(id: BlockChildID):
    return f"block:{id.project}/{id.block}/{id.version}"


def version_id_to_local_path(id: BlockChildID):
    return f"images/{id.project}_{id.block}_{id.version}"


def localize_image_from_top_level_block(
    session: Session, assets_folder: str, version: BlockVersion
):
    block_path = version_id_to_block_path(version.id)
    local_path = version_id_to_local_path(version.id)

    image_block, local_path_with_extension = get_image_block(
        session, assets_folder, block_path, local_path
    )

    content = (
        IMAGE_LATEX_TPL.replace(VERSION_ID, local_path_with_extension)
        .replace(CAPTION, image_block.caption)
        .replace(LABEL, get_fast_hash())
    )

    return f"\n\n{content}\n"
