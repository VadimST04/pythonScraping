import scrapy


class WorldometerSpider(scrapy.Spider):
    """
    This Spider is designed to scrape population data by country from the Worldometer website.
    It navigates through the list of countries and their population details.
    """

    name = 'worldometer'
    allowed_domains = ['www.worldometers.info']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        """
        Parse the list of countries and their links from the response.
        :param response: The HTTP response from the request.
        :yield: Yields a requests to parse specific country data.
        """
        countries = response.xpath('//td/a')

        for country in countries:
            country_name = country.xpath('.//text()').get()
            link = country.xpath('.//@href').get()

            yield response.follow(url=link, callback=self.parse_country, meta={'country': country_name})

    def parse_country(self, response):
        """
        Parse specific country population data from the response.
        :param response: The HTTP response from the request.
        :yield: Yields a dictionary containing specific country population data.
        """
        country = response.request.meta['country']
        rows = response.xpath('(//table[contains(@class, "table")])[1]/tbody/tr')
        for row in rows:
            year = row.xpath('.//td[1]/text()').get()
            population = row.xpath('.//td[2]/strong/text()').get()

            yield {
                'country': country,
                'year': year,
                "population": population,
            }
