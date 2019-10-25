from typing import Callable, List, Any
import bs4
import re

from utils import split_into_tokens


def prepare_soup_mutator_set(
    mutators: List[Callable[[bs4.BeautifulSoup], bs4.BeautifulSoup]]
):
    """
    This wrapper function is needed to apply
    several html tree transformations
    without parsing html every time.
    """
    def soup_mutator_set(data: bytes) -> bytes:
        soup = bs4.BeautifulSoup(data, "lxml")
        for mutator in mutators:
            try:
                soup = mutator(soup)
            except Exception as e:
                print("Unable to apply '{}' mutator: {}".format(
                    mutator.__name__, e))
        return soup.encode()
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
    urls_to_replace: List[str],
    svg: bool = True,
) -> Callable[[bs4.BeautifulSoup], bs4.BeautifulSoup]:
    def make_links_local(soup: bs4.BeautifulSoup) -> bs4.BeautifulSoup:
        urls_regexp = re.compile("({})".format("|".join(urls_to_replace)))
        selector_templates = [
            ('a[href^="{}"]', 'href'),
            ('use[xlink\:href^="{}"]', 'xlink:href'),
        ]
        for template, attr in selector_templates:
            selectors = [template.format(u) for u in urls_to_replace]
            for tag in soup.select(",".join(selectors)):
                tag[attr] = urls_regexp.sub("http://" + local_url, tag[attr])
        return soup
    return make_links_local
