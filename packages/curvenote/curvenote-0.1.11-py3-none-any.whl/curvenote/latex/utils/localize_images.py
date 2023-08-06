from collections import namedtuple

ImageFormats = {"image/png": "png", "image/jpeg": "jpg", "image/gif": "gif"}
ImageSummary = namedtuple("ImageSummary", ["content", "block_paths", "local_paths"])
