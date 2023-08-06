BLOCK_ID_REGEX = r"block:[A-Za-z0-9]{20}/[A-Za-z0-9]{20}/[0-9]+"
CAPTION_BLOCK_ID_REGEX = r"block:[A-Za-z0-9]{20}/[A-Za-z0-9]{20}/[0-9]+.caption"

INLINE_IMAGE_BLOCK_REGEX = (
    r".*\\includegraphics.*{(block:[A-Za-z0-9]{20}/[A-Za-z0-9]{20}/[0-9]+)}.*\\*"
)
CAPTION_COMMAND_REGEX = r".*\\caption{(" + CAPTION_BLOCK_ID_REGEX + r")}.*\\*"
LABEL_COMMAND_REGEX = r".*\\label{([A-Za-z0-9_-]*)}.*\\*"
OUTPUT_IMAGE_BLOCK_REGEX = (
    r".*\\includegraphics.*{(block:[A-Za-z0-9]{20}/[A-Za-z0-9]{20}/[0-9]+"
    r"-output-[0-9]+)}.*\\*"
)
OUTPUT_SVG_BLOCK_REGEX = (
    r".*\\includesvg.*{(block:[A-Za-z0-9]{20}/[A-Za-z0-9]{20}/[0-9]+"
    r"-output-[0-9]+)}.*\\*"
)
INLINE_CITATION_BLOCK_REGEX = r"\\cite[pt]?{(block:[A-Za-z0-9]{20}/[A-Za-z0-9]{20})}"
