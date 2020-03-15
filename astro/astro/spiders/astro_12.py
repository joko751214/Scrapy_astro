# -*- coding: utf-8 -*-
import scrapy
from ..items import AstroItem


class Astro12Spider(scrapy.Spider):
	name = 'astro_12'
	allowed_domains = ['astro.click108.com.tw']
	start_urls = []
	for i in range(12):
		start_urls.append("http://astro.click108.com.tw/daily_{}.php?iAstro={}".format(i,i))

	def parse(self, response):
		for each in response.xpath("//div[@class='TODAY_FORTUNE']"):
			item = AstroItem()
			item['date'] = each.xpath('//*[@id="iAcDay"]/option[4]/text()').extract()[0]
			item['astro_name'] = each.xpath('//div[@class="TODAY_CONTENT"]/h3/text()').extract()[0][2:5]
			item['title_all_score'] = each.xpath('//span[@class="txt_green"]/text()').extract()[0][4:9]
			item['title_love_score'] = each.xpath('//span[@class="txt_pink"]/text()').extract()[0][4:9]
			item['title_work_score'] = each.xpath('//span[@class="txt_blue"]/text()').extract()[0][4:9]
			item['title_money_score'] = each.xpath('//span[@class="txt_orange"]/text()').extract()[0][4:9]
			item['title_all_desc'] = each.xpath('//div[@class="TODAY_CONTENT"]/p[2]/text()').extract()[0]
			item['title_love_desc'] = each.xpath('//div[@class="TODAY_CONTENT"]/p[4]/text()').extract()[0]
			item['title_work_desc'] = each.xpath('//div[@class="TODAY_CONTENT"]/p[6]/text()').extract()[0]
			item['title_money_desc'] = each.xpath('//div[@class="TODAY_CONTENT"]/p[8]/text()').extract()[0]
			yield item
		'''
		soup = BeautifulSoup(response.text, 'lxml')
		titles = soup.select('h2.entry-title')
		for t in titles:
			meta = {
				'title': t.text,
				'link': t.select_one('a').get('href')
			}
			# 將下面的部分改寫成上面的meta
			# link = t.select_one('a').get('href')
			# title = t.text

			# 這邊的meta是讓article_parser這個function可以使用
			yield scrapy.Request(meta['link'], callback=self.article_parser, meta=meta)
		self.num += 1
		next_page = self.start_urls[0] +'/page/'+ str(self.num)
		yield scrapy.Request(next_page, callback=self.parse)
		'''

	def article_parser(self, response):
		soup = BeautifulSoup(response.text, 'lxml')
		article = TranewsItem()
		article['title'] = response.meta['title']
		article['link'] = response.meta['link']
		
		contents = soup.select('div.entry-content p')
		article['content'] = ''
		for content in contents:
			article['content'] = article['content'] + content.text 
		article['img'] = soup.select_one('img').get("src")
		article['time'] = soup.select_one('span.entry-date').text
		return article
