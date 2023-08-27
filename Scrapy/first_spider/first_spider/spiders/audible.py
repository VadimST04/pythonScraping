import scrapy


class AudibleSpider(scrapy.Spider):
    """
    This Spider is designed to scrape book information, including title, author, and length,
    from the Audible website. It navigates through multiple pages of search results.
    """

    name = 'audible'
    allowed_domains = ['www.audible.de']

    # start_urls = ['https://www.audible.de/search']

    def start_requests(self):
        """
        Generate initial requests to start scraping and changes User-Agent.
        :yield: Yields an initial request with url, callback and headers.
        """
        yield scrapy.Request(url='https://www.worldometers.info/world-population/population-by-country/',
                             callback=self.parse,
                             headers={
                                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'})

    def parse(self, response):
        """
        Parse the book data form all pages from the response.
        :param response: The HTTP response from the request.
        :yield: Yields a dictionary with received book data (title, author, length)
        then yields request with parse function as a callback if the next page exists.
        """
        product_container = response.xpath(
            '//div[@class="adbl-impression-container "]//li[contains(@class, "productListItem")]')

        for product in product_container:
            book_title = product.xpath('.//h3/a/text()').get()
            book_author = product.xpath('.//li[contains(@class, "authorLabel")]/span/a/text()').getall()
            book_length = product.xpath('.//li[contains(@class, "runtimeLabel")]/span/text()').get()

            yield {
                'title': book_title,
                'author': book_author,
                'length': book_length,
                'User-Agent': response.request.headers['User-Agent'],
            }

            pagination = response.xpath('//ul[contains(@class, "pagingElements ")]')
            next_page_url = pagination.xpath('.//span[contains(@class, "nextButton")]/a/@href').get()

            if next_page_url:
                yield response.follow(url=next_page_url, callback=self.parse,
                                      headers={
                                          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'})
