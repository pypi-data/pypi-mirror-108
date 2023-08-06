import re
from typing import List
from .localize_images import ImageSummary


def patch_local_images_from_tex_block(regex_matcher: str, content: str):
    """
    Take a peice of tex content that we expect to contain only one includegraphics directive
    get the remote path, assign a new local path and retrun a structure that can be parsed
    """
    updated_content = content
    block_paths: List[str] = []
    local_paths: List[str] = []
    matches = re.finditer(regex_matcher, content)
    for match in matches:
        block_path = match[1]
        hash_segment = block_path[6:]
        local_segment = hash_segment.replace("/", "_")
        local_path = block_path.replace("block:", "images/").replace(
            hash_segment, local_segment
        )
        updated_content = updated_content.replace(block_path, local_path)
        block_paths.append(block_path)
        local_paths.append(local_path)

    return ImageSummary(
        content=updated_content,
        block_paths=block_paths,
        local_paths=local_paths,
    )
