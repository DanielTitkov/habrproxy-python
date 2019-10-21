import re
import html

from typing import List


def split_into_tokens(string: str) -> List[str]:
    string = amend_html_symbols(string)
    return re.findall(r"[\w']+|[\s.,!?+;-_-]", string)


def amend_html_symbols(string: str) -> str:
    return html.unescape(string)
