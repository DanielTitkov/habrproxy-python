from typing import Callable, List, Any
import bs4

from utils import split_into_tokens, concatenate_tokens


def prepare_append_symbol_if_length(
    symbol: str,
    length: int,
    ignore_types: List[Any], 
    ignore_tag_names: List[str],
) -> Callable:
    def append_symbol_if_length(soup: bs4.BeautifulSoup) -> bs4.BeautifulSoup:
        for child in soup.html.findChildren(string=True, recursive=True):
            if all([
                child.string,
                type(child) not in ignore_types,
                child.parent.name not in ignore_tag_names,
            ]):
                mutated_tokens = [t + symbol if len(t) == length else t 
                    for t in split_into_tokens(child.string)]
                mutated_string = concatenate_tokens(mutated_tokens)
                child.replace_with(mutated_string)
        return soup
    return append_symbol_if_length


def prepare_soup_mutator_set(mutators: List[Callable]):
    """
    This wrapper function is needed to apply 
    several html tree transformations
    without parsing html every time.
    """
    def soup_mutator_set(data: bytes) -> bytes:
        soup = bs4.BeautifulSoup(data, "html.parser")
        for mutator in mutators:
            soup = mutator(soup)
        mutated_data = bytes(str(soup), encoding='utf-8')
        return mutated_data
    return soup_mutator_set


def prepare_make_links_local(local_url: str) -> Callable:
    def make_links_local(data: bytes) -> bytes:
        print(local_url)
        mutated_data = data
        return mutated_data
    return make_links_local
