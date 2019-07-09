import scrapy
import datetime as dt
from bs4 import BeautifulSoup as bs

from newslib.items import NewslibItem as nlitem

class Spiegel_Online_Archive_Spider(scrapy.Spider):
    name = "spiegel_online_archive"
    start_urls = []

    def __init__(self):
        self.populate_urls()

    def populate_urls(self):
        start = dt.datetime.strptime("01-01-2000", "%d-%m-%Y")
        end = dt.datetime.today()
        date_generated = [start + dt.timedelta(days=x) for x in range(0, (end - start).days)]

        def cleanStr(date):
            return(date[8:10] + '.' + date[5:7] + '.' + date[:4] )

        for d in date_generated:
            self.start_urls.append('https://www.spiegel.de/nachrichtenarchiv/artikel-' + cleanStr(str(d)) + '.html')

    def parse(self, response):
        soup = bs(response.text, 'lxml')
        li = soup.find('div', 'column-wide').find_all('li')

        for l in li:
            yield scrapy.Request('https://www.spiegel.de' + l.find('a')['href'], self.parse_article_site)

    def parse_article_site(self, response):
        item = nlitem()
        soup = bs(response.text, 'lxml')

        for i in soup.time.contents:
            pass
        item['headline'] = soup.h1.string
        item['subline'] = soup.p.string

        l = ''
        for i in soup.find('div', {"class":"article-section"}).find_all('p'):
            l = l + i.string

        item['text'] = l

        yield item
