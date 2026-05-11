# scrapy-poet Reference

Concise reference for using web-poet page objects in Scrapy spiders. For full docs
see https://scrapy-poet.readthedocs.io/

## Setup

```python
# settings.py
ADDONS = {
    "scrapy_poet.Addon": 300,
}
SCRAPY_POET_DISCOVER = ["my_project.pages"]
```

## Using page objects in spiders

Page objects are injected into spider callbacks via type annotations:

```python
import scrapy
from scrapy_poet import DummyResponse

from my_project.pages.example_com import ProductPage, NavigationPage


class ExampleSpider(scrapy.Spider):
    name = "example"
    start_urls = ["https://example.com"]

    async def parse(self, response: DummyResponse, nav: NavigationPage):
        nav_item = await nav.to_item()
        for link in nav_item.items or []:
            yield scrapy.Request(link["url"], callback=self.parse_product)

    async def parse_product(self, response: DummyResponse, page: ProductPage):
        yield await page.to_item()
```

### DummyResponse

When a callback only uses the injected page object and doesn't need the Scrapy
`response`, annotate the parameter as `response: DummyResponse`. This tells
scrapy-poet that no download is needed for the response object — the page object's
dependencies are provided separately (e.g., via Zyte API provider).

### Async callbacks

Spider callbacks that use page objects should be `async def`, since page object
methods (like `to_item()`) are async.

## handle_urls

`@handle_urls` registers a page object for a URL pattern. This serves two purposes:
- **Documentation** — declares which domain/path a page object is designed for
- **Generic spiders** — enables spiders that request an item class (e.g., `ProductItem`),
  and the framework automatically picks the right page object for the current URL

```python
from web_poet import handle_urls, WebPage, Returns

@handle_urls("example.com")
class ProductPage(WebPage, Returns[ProductItem]): ...
```

- `"example.com"` — matches domain and subdomains
- `"example.com/products/"` — matches specific path prefix

Page objects can also be injected directly by type annotation in spider callbacks
without `@handle_urls`. But `@handle_urls` is needed for generic/multi-site spiders
where the framework selects the page object based on URL and item type.

Modules containing `@handle_urls` decorators must be listed in `SCRAPY_POET_DISCOVER`
for scrapy-poet to find them.
