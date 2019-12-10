# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import xlsxwriter

class RapplerPipeline(object):
    length = 0

    def open_spider(self, spider):
        self.wb = xlsxwriter.Workbook('rappler.xlsx')
        self.sheet = self.wb.add_worksheet('Rappler Articles')
        self.sheet.write(0, 0, 'Article Name')
        self.sheet.write(0, 1, 'Subheader')
        self.sheet.write(0, 2, 'Category')

    def process_item(self, item, spider):
        self.length += 1
        self.sheet.write(self.length, 0, item['title'])
        self.sheet.write(self.length, 1, item['content'])
        self.sheet.write(self.length, 2, item['category'])
        return item

    def close_spider(self, spider):
        self.wb.close()
