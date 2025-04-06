import logging
import re
from pathlib import Path

from turnstile_solver.proxy import Proxy

_PROXY_PARSE_RE = re.compile(r'')

logger = logging.getLogger(__name__)


class ProxyProvider:
  def __init__(self, proxies_fp: str | Path):
    self.proxies_fp = proxies_fp
    self._index = 0
    self._proxies: list[Proxy] = []

  def get(self) -> Proxy | None:
    if not self._proxies:
      return
    proxy = self._proxies[self._index]
    self._index = (self._index + 1) % len(self._proxies)
    return proxy

  def load(self):
    with open(self.proxies_fp, 'rt') as f:
      proxyCount = 0
      for line in f.readlines():
        if not (line := line.strip()) or line.startswith('#'):
          continue
        parts = line.split('@')
        server = parts[0]
        if len(parts) > 1:
          username, password = parts[1].split(':')
        else:
          username = password = None
        self._proxies.append(Proxy(server, username, password))
        proxyCount += 1
      logger.info(f"{proxyCount} proxies loaded from '{self.proxies_fp}'")
