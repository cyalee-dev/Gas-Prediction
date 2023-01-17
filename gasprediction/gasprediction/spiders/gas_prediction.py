import scrapy

'''scrapy runspider gasprediction/spiders/gas_prediction.py'''
'''scrapy runspider gasprediction/spiders/gas_prediction.py -o gasprediction.json'''

class GasPredictionSpider(scrapy.Spider):
    name = 'gas_prediction'
    allowed_domains = ['gaswizard.ca']
    start_urls = ['https://gaswizard.ca/gas-price-predictions/']

    def parse(self, response):
        # title = response.css('div.price-date::text').get()
        title = response.xpath('//div[@class="price-date"]/text()').get()
        cityname = response.xpath('//td[@class="gwgp-cityname"]/text()').getall()
        gasprice = response.xpath('//td[@class="gwgp-price"]/text()').getall()
        cityname = [i.strip(': ') for i in cityname]
        gasprice = [j.strip('\r\n\t\t\t\t\t\t') for j in gasprice]
        while("" in gasprice):
            gasprice.remove("")
        citycount = len(cityname)
        gaspricecount = len(gasprice)

        return {"title": title, "cityname" : cityname, "gasprice" : gasprice, "citycount" : citycount, "gaspricecount" : gaspricecount}
        pass
