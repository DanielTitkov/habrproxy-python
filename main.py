import bs4
from http.server import ThreadingHTTPServer

from proxy import Proxy
from handlers import MutatorHandler
from mutators import (
    prepare_make_links_local,
    prepare_soup_mutator_set,
    prepare_append_symbol_if_length,
)

if __name__ == "__main__":
    target_url = "https://habr.com/en/all/"
    local_host = "localhost"
    local_port = 9000
    local_url = "{}:{}".format(local_host, local_port)

    proxy = Proxy(
        target_url=target_url,
        local_host=local_host,
        local_port=local_port,
        server=ThreadingHTTPServer,
        handler=MutatorHandler,
        mutators=[
            prepare_soup_mutator_set(
                mutators=[
                    prepare_append_symbol_if_length(
                        symbol="™",
                        length=6,
                        ignore_types=[bs4.element.Comment],
                        ignore_tag_names=["script", "title", "code",
                                          "style", "svg", "math", "g"],
                    ),
                    prepare_make_links_local(
                        local_url=local_url,
                        urls_to_replace=["https://habr.com"],
                        svg=True,
                    )
                ]
            )
        ],
    )

    proxy.run()
