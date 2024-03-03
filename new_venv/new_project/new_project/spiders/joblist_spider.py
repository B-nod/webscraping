import scrapy
from new_project.items import NewProjectItem
import pandas as pd


class JoblistSpiderSpider(scrapy.Spider):
    name = "joblist_spider"
    page_number = 2
    allowed_domains = ["www.reed.co.uk"]
    start_urls = ["https://www.reed.co.uk/jobs/data-analyst-jobs"]
    base_url = 'https://www.reed.co.uk/jobs/data-analyst-jobs'

    def parse(self, response):
        job_item = NewProjectItem()
        for sel in response.xpath('//header') :
            job_item['title'] = sel.xpath('h2/a/text()').extract()
            job_item['url'] = sel.xpath('h2/a/@href').extract()
            job_item['salary'] = sel.xpath('ul/li[1]/text()').extract()
            job_item['location'] = sel.xpath('ul/li[2]/text()').extract()
            types = sel.xpath('ul/li[3]/text()').extract()
            type = ', '.join(types)
            li = list(type.split(', '))
            job_item['contract_type'] = li[::2]
            job_item['job_type'] = li[1::2]

            yield job_item
            

        # next_page_partial_url  = response.xpath('//ul/li[@class="page-item"]/a/@href').extract_first()
        # nex_page_url = self.base_url + next_page_partial_url 

        # yield scrapy.Request(nex_page_url, callback=self.parse)
            
        next_page = 'https://www.reed.co.uk/jobs/data-analyst-jobs?pageno=' + str(JoblistSpiderSpider.page_number)
        if JoblistSpiderSpider.page_number <= 119:
            JoblistSpiderSpider.page_number += 1
            yield response.follow(next_page, callback= self.parse)
        
       
