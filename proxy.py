import functools 
from typing import Any, List, Callable


class Proxy:
    def __init__(
        self,
        target_url: str,
        local_host: str,
        local_port: int,
        server: Any,
        handler: Any,
        mutators: List[Callable[[bytes], bytes]],
    ) -> None:
        self.target_url = target_url
        self.local_host = local_host
        self.local_port = local_port
        self.server = server
        self.handler = handler
        self.mutators = mutators

    def run(self) -> None:
        handler = functools.partial(self.handler, self.target_url, self.mutators)
        server = self.server((self.local_host, self.local_port), handler)
        print("Starting server at localhost:{}".format(self.local_port))

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("Shutting down proxy")

        server.server_close()
