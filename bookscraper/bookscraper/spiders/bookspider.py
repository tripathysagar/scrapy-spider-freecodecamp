import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.xpath('//article[@class="product_pod"]')

        for book in books:
            book_url = book.css("h3 a").attrib['href']

            if 'catalogue/' in book_url:
                book_page_url = 'https://books.toscrape.com/' + book_url
            else:
                book_page_url = 'https://books.toscrape.com/catalogue/' + book_url
            
            yield scrapy.Request(book_page_url, callback=self.parse_book_page)
        
        next_page = response.xpath('//li[@class="next"]/a').attrib['href']

        if next_page:
            if 'catalogue/' in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
        
            yield response.follow(next_page_url)

    def parse_book_page(self, response):
        book = response.css('div.product_main')
        table_rows = response.css("table tr")

        yield{
            'url': response.url,
            'title': book.css("h1 ::text").get(),
            'price': book.css("p ::text").get(),
            'stars': book.css("p")[2].attrib["class"].split(" ")[1],
            'category': book.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
            'description': book.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),

            'UPC': table_rows[0].css("td ::text").get(),
            "Product_Type": table_rows[1].css("td ::text").get(),
            "Price_excl_tax": table_rows[2].css("td ::text").get(),
            "Price_incl_tax": table_rows[3].css("td ::text").get(),
            "Tax": table_rows[4].css("td ::text").get(),
            "Availability": table_rows[5].css("td ::text").get(),
            "Number_of_reviews": table_rows[6].css("td ::text").get()
        }