import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.xpath('//article[@class="product_pod"]')

        for book in books:
            yield {
                'name': book.css("h3 a::text").get(),
                'price': book.css(".product_price .price_color").get(),
                'url': book.css("h3 a").attrib['href']
            }
        
        next_page = response.xpath('//li[@class="next"]/a').attrib['href']

        if next:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
        
            yield response.follow(next_page_url)
