# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import RatemdsSpiderItem
from urlparse import urljoin
import json


class RatemdsSpider(CrawlSpider):
    name = 'ratemds'
    allowed_domains = ['ratemds.com']
    
    def start_requests(self):
    	#headers = {'User-Agent' :'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36', 'Content-Type': 'application/json'}
    
    	for x in range(46,50):
    		url = "https://ratemds.com/api/doctor/{0}".format(x)
    		print url
        	yield scrapy.Request(url, callback=self.parse_details)

    def parse_details(self, response):

    	i = RatemdsSpiderItem()

        result = response.body
        result = ''.join(result)
        json_data = json.loads(result)
        i['name'] = json_data['full_name']
        i['api_url'] = response.url
        tmp_link = json_data['url']
        absoulate_link = response.urljoin(tmp_link)
        i['link'] = absoulate_link
        i['gender'] = json_data['gender']
        i['speciality'] = json_data['specialty_name']
        i['practice_name'] = json_data['location']['name']
        try:
        	i['edu_name'] = json_data['doctor_schools'][0]['school']['name']
        	i['completion_year'] = json_data['doctor_schools'][0]['graduation_year']
        except:
        	pass
        
        #i['completion_year'] = json_data['doctor_schools'][0]['graduation_year']
        i['street_address'] = json_data['location']['address']
        i['city'] = json_data['location']['city']['name']
        i['state'] = json_data['location']['city']['province_name']
        state_slug = json_data['location']['city']['province_slug']
        i['state_slug'] = state_slug.upper()
        i['country'] = json_data['location']['city']['country_name']
        i['zip_code'] = json_data['location']['postal_code']
        i['phone'] = json_data['location']['phone_number']
        i['reviewCount'] = json_data['rating']['count']
        i['average_score'] = json_data['rating']['average']

        yield i
