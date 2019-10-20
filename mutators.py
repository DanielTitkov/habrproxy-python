from typing import Callable, List, Any
import bs4
import re

from utils import split_into_tokens


def prepare_soup_mutator_set(mutators: List[Callable[[bytes], bytes]]):
    """
    This wrapper function is needed to apply 
    several html tree transformations
    without parsing html every time.
    """
    def soup_mutator_set(data: bytes) -> bytes:
        soup = bs4.BeautifulSoup(data, "html.parser")
        for mutator in mutators:
            try:
                soup = mutator(soup)
            except Exception as e:
                print("Unable to apply '{}' mutator: {}".format(
                    mutator.__name__, e))
        mutated_data = bytes(str(soup), encoding='utf-8')
        return mutated_data
    return soup_mutator_set


def prepare_append_symbol_if_length(
    symbol: str,
    length: int,
    ignore_types: List[Any],
    ignore_tag_names: List[str],
) -> Callable[[bs4.BeautifulSoup], bs4.BeautifulSoup]:
    def append_symbol_if_length(soup: bs4.BeautifulSoup) -> bs4.BeautifulSoup:
        for child in soup.html.findChildren(string=True, recursive=True):
            if all([
                child.string,
                type(child) not in ignore_types,
                child.parent.name not in ignore_tag_names,
            ]):
                mutated_tokens = [t + symbol if len(t) == length else t
                                  for t in split_into_tokens(child.string)]
                child.replace_with(''.join(mutated_tokens))
        return soup
    return append_symbol_if_length


def prepare_make_links_local(
    local_url: str,
    urls_to_replace: List[str]
) -> Callable[[bs4.BeautifulSoup], bs4.BeautifulSoup]:
    def make_links_local(soup: bs4.BeautifulSoup) -> bs4.BeautifulSoup:
        selectors = ['a[href^="{}"]'.format(u) for u in urls_to_replace]
        urls_regexp = re.compile("({})".format("|".join(urls_to_replace)))
        for a in soup.select(",".join(selectors)):
            a['href'] = urls_regexp.sub("http://" + local_url, a['href'])
        return soup
    return make_links_local
