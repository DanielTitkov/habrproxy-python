from http.server import BaseHTTPRequestHandler
import urllib.request, urllib.parse
from typing import Any, List


class MutatorHandler(BaseHTTPRequestHandler):
    def __init__(self, target_url: str, mutators: List[Any], *args: Any, **kwargs: Any) -> None:
        self.target_url = target_url
        self.mutators = mutators
        super().__init__(*args, **kwargs)

    def do_HEAD(self) -> None:
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self) -> None:
        self.do_HEAD()
        url = urllib.parse.urljoin(self.target_url, self.path)
        data = urllib.request.urlopen(url).read()
        mutated_data = self.apply_mutators(data)
        self.wfile.write(mutated_data)

    def apply_mutators(self, data: bytes) -> bytes:
        mutated_data = data
        for mutator in self.mutators:
            mutated_data = mutator(mutated_data)
        return mutated_data
