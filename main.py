import bs4
import argparse
from http.server import ThreadingHTTPServer

from proxy import Proxy
from handlers import MutatorHandler
from mutators import (
    prepare_make_links_local,
    prepare_soup_mutator_set,
    prepare_append_symbol_if_length,
)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Harb Proxy Reader')
    parser.add_argument('-l', '--local',
                        help="Local host",
                        default="localhost")
    parser.add_argument('-p', '--port',
                        help="Local port",
                        type=int, default=8018)
    parser.add_argument('-t', '--target',
                        help="Site to proxy",
                        default="https://habr.com/ru/all/")
    args = parser.parse_args()

    local_url = "{}:{}".format(args.local, args.port)

    proxy = Proxy(
        target_url=args.target,
        local_host=args.local,
        local_port=args.port,
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
