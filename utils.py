import re

from typing import List


def split_into_tokens(string: str) -> List[str]:
    return re.findall(r"[\w']+|[\s.,!?;]", string)


def concatenate_tokens(tokens: List[str]) -> str:
    return ''.join(tokens)
