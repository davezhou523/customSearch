import scrapy
import re


class ContactSpider(scrapy.Spider):
    name = 'contact_spider'

    # 这里设置你从Google Custom Search获取的URL列表
    start_urls = [
        'https://www.epilepsy.com/contact-us',
        # 添加更多的URL...
    ]

    def parse(self, response):
        # 使用正则表达式匹配邮箱
        print(response.text)
        emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text)

        # 使用正则表达式匹配电话号码
        phones = re.findall(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', response.text)

        yield {
            'url': response.url,
            'emails': emails,
            'phones': phones,
        }
