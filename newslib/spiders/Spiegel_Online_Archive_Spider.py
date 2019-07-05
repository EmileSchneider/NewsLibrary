import scrapy
import datetime as dt

class Spiegel_Online_Archive_Spider(scrapy.Spider):
    name = "spiegel_online_archive"
    start_urls = []

    def populateUrls(self):
        start = dt.datetime.strptime("01-01-2000", "%d-%m-%Y")
        end = dt.datetime.today()
        date_generated = [start + dt.timedelta(days=x) for x in range(0, (end - start).days)]

        def cleanStr(date):
            return(date[8:10]  + '.' + date[5:7] + '.' + date[:4] )

        for d in date_generated:
            self.start_urls.append('https://www.spiegel.de/nachrichtenarchiv/artikel-' + cleanStr(str(d)) + '.html')


s = Spiegel_Online_Archive_Spider()
s.populateUrls()