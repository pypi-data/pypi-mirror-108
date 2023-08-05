"""Template globals."""

from pprint import pformat
from textwrap import dedent

import emoji
from understory.web import tx
from understory.web.indie.micropub import discover_post_type
from understory.web.indie.webmention import get_mentions

__all__ = ["pformat", "tx", "get_mentions", "discover_post_type",
           "dedent", "emoji"]
