from http.server import BaseHTTPRequestHandler
import urllib.request
import urllib.parse
from typing import Any, List


class MutatorHandler(BaseHTTPRequestHandler):
    def __init__(
        self,
        target_url: str,
        mutators: List[Any],
        *args: Any, **kwargs: Any
    ) -> None:
        self.target_url = target_url
        self.mutators = mutators
        super().__init__(*args, **kwargs)

    def do_HEAD(self, content_type: str = "text/html") -> None:
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self) -> None:
        url = urllib.parse.urljoin(self.target_url, self.path)
        response = urllib.request.urlopen(url)
        content_type = response.headers.get("Content-type")
        data = response.read()

        self.do_HEAD(content_type)

        try:
            if "text/html" in content_type:
                mutated_data = self.apply_mutators(data)
                self.wfile.write(mutated_data)
            else:
                self.wfile.write(data)
        except BrokenPipeError:
            return

    def apply_mutators(self, data: bytes) -> bytes:
        mutated_data = data
        for mutator in self.mutators:
            mutated_data = mutator(mutated_data)
        return mutated_data
