import scrapy

class RapplerSpider(scrapy.Spider):
    name = "rappler"
    custom_settings = {
        'ITEM_PIPELINES': {
            'rappler.pipelines.RapplerPipeline' : 900
        }
    }

    def start_requests(self):
        url = lambda x, y : 'https://www.rappler.com/previous-articles/arti \
                            cles?filterMeta='+x+'&userSearch=1&start='+str(y)
        categories = [
            'Sports',
            'Crime',
            'Business',
            'Technology'
        ]
        limit = [
            2550,
            2300,
            1250,
            1900
        ]
        for idx, category in enumerate(categories):
            count = 0 
            while count <= limit[idx]:
                yield scrapy.Request(url(category, count),
                                    meta = {'category' : category},
                                    callback = self.parse)
                count += 50


    def parse(self, response):
        titles = response.xpath('//*[@id="article-finder-result"]//*[contains(@class, "rappler-headline")]/text()')
        subtitles = response.xpath('//*[@id="article-finder-result"]//div[@class="padding bottom"]/following-sibling::p')
    
        titles = [x.get() for x in titles]

        full_texts = [x.xpath('text()').get() for x in subtitles]

        items = []
        
        for idx, title in enumerate(titles):
            items.append({
                'title': title,
                'content': full_texts[idx],
                'category': response.meta['category']
            })
        
        return items