import logging

from patchright.async_api import BrowserContext, Page
from turnstile_solver.pool import Pool

from .constants import MAX_PAGES_PER_CONTEXT

logger = logging.getLogger(__name__)


class PagePool(Pool):
  def __init__(self,
               context: BrowserContext,
               max_pages: int = MAX_PAGES_PER_CONTEXT,
               ):
    self.context = context

    async def itemGetter():
      return await self.context.new_page()

    super().__init__(
      size=max_pages,
      item_getter=itemGetter,
    )
