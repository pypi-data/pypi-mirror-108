import logging
from typing import List, Optional, Union

from curvenote.latex import utils

from ..client import Session
from ..models import Block, BlockFormat, BlockKind, BlockVersion, ChildrenList, Project
from . import utils
from .block_version import LatexBlockVersion

logger = logging.getLogger()


class LatexArticle:
    """
    Class to represent an article in the latex project.
    With the abilty to fetch, localize its assets and write itself to file.
    """

    def __init__(
        self, session: Session, project_id: Union[str, Project], article_id: str
    ):
        self.session = session
        self.project_id = project_id
        self.article_id = article_id
        self.block: Block = None
        self.version: BlockVersion = None
        self.children: ChildrenList = None
        self.content: str = ""
        # TODO obvious one to centralise in project or someway
        self.users = []

    @property
    def title(self):
        if self.block:
            return self.block.title
        return ""

    @property
    def description(self):
        if self.block:
            return self.block.description
        return None

    @property
    def authors(self):
        if self.block:
            return self.block.authors
        return []

    @property
    def author_names(self):
        names = []
        for author in self.authors:
            if author.user:
                for user in self.users:
                    if user.id == author.user:
                        names.append(user.display_name)
            else:
                names.append(author.plain)
        return names

    @property
    def date(self):
        if self.version:
            return self.version.date or self.version.date_created
        return None

    def oxalink(self, base: str):
        if self.version is None:
            return None
        v = self.version
        return f"{base}/oxa:{v.id.project}/{v.id.block}.{v.id.version}"


    def fetch(self, version: Optional[int] = None):
        """Download article and all children in Latex format

        Raises ValueError if download fails.
        """
        logging.info("article.fetch")
        block = self.session.get_block(
            self.project_id, self.article_id, kind=BlockKind.article
        )
        logging.info("article.fetch got block")
        version_to_fetch = version or block.latest_version
        children = self.session.get_version_with_children(
            block, version_to_fetch, fmt=BlockFormat.tex
        )
        if len(children.errors) > 0:
            logger.error("There were errors fetching some children")
            for error in children.errors:
                logger.error(error)

        if children.versions.items[0].kind != BlockKind.article:
            raise ValueError("Expected first child to be an article")
        self.block = children.blocks.items[0]
        self.version, *self.children = children.versions.items
        logger.info(
            f"Processing Article: {self.version.id.project}/"
            f"{self.version.id.block}/versions/{self.version.id.version}"
        )

    def localize(
        self,
        session: Session,
        assets_folder: str,
        reference_list: List[utils.LocalReferenceItem],
    ):
        """Parse article content and pull assets to local storage

        - images
        - authors
        - citations

        TODO: this is turning into a double dispatchy thing, maybe article just holds a
        reference to the project
        """
        logging.info("Localizing referenced content")
        self._localize_authors(session)
        logging.info("Localized authors")
        self._localize_content(session, assets_folder, reference_list)
        logging.info("Localized content and references")

    def write(self, filepath: str):
        with open(filepath, "w+") as file:
            file.write(self.content)

    def _localize_authors(self, session: Session):
        for author in self.authors:
            if author.user is not None:
                try:
                    self.users.append(session.get_user(author.user))
                except ValueError as err:
                    logger.info(f"Could not get user {author.user}: {err}")
                    continue

    def _localize_content(
        self, session: Session, assets_folder: str, reference_list: List[str]
    ):
        """
        Ignores blocks of any type other than Content and Output.
        """
        concatenated_content = ""
        for i, child in enumerate(self.children):
            block = LatexBlockVersion(session, child)

            try:
                block.localize(assets_folder, reference_list)
                if i == 0:
                    concatenated_content += f"{block.content}\n"
                else:
                    concatenated_content += f"\n\n{block.content}\n"
            except ValueError:
                continue

        self.content = concatenated_content
