import scrapy
import json

class FemaleSpider(scrapy.Spider):
    name = "female"
    allowed_domains = ["jiayuan.com"]

    SEARCH_TEMPLATE = {"sex":"f",
                       "key":"",
                       "stc":"1:31,2:28.36,3:155.170,23:1",
                       "sn":"default",
                       "sv":"1",
                       "p":"1",
                       "f":"1",
                       "listStyle":"bigPhoto",
                       "pri_uid":"0",
                       "jsversion":"v5"};
    SEARCH_URL = "http://search.jiayuan.com/v2/search_v2.php"

    MAX_PAGE_NUM = 10

    NAME = None
    PWD = None

    def __init__(self, name=None, pwd=None, *args, **kwargs):
        super(FemaleSpider, self).__init__(*args, **kwargs)
        self.NAME = name
        self.PWD = pwd

    def start_requests(self):
        return [scrapy.Request("http://login.jiayuan.com/", meta = {'cookiejar' : 1}, callback = self.post_login)]

    def post_login(self, response):
        return [scrapy.FormRequest.from_response(response,
                            meta = {'cookiejar' : response.meta['cookiejar']},
                            formdata = {
                            'name': self.NAME,
                            'password': self.PWD
                            },
                            callback = self.after_login
                            )]

    def after_login(self, response):
        pageNum = 1

        formdata = self.SEARCH_TEMPLATE
        formdata["p"] = str(pageNum)

        yield scrapy.FormRequest(self.SEARCH_URL, meta = {'cookiejar' : response.meta['cookiejar'], "page_num": pageNum}, callback=self.parse, formdata=formdata)

    def parse(self, response):
        responseText = response.body_as_unicode()
        start = len("##jiayser##")
        end = len(responseText) - len("##jiayser##//")

        jsonresponse = json.loads(responseText[start:end])

        users = jsonresponse['userInfo']

        for user in users:
            yield user

        if len(users) > 0:
            pageNum = response.meta['page_num']
            pageNum = pageNum + 1

            if pageNum <= self.MAX_PAGE_NUM:
                formdata = self.SEARCH_TEMPLATE
                formdata["p"] = str(pageNum)

                yield scrapy.FormRequest(self.SEARCH_URL, meta = {'cookiejar' : response.meta['cookiejar'], "page_num": pageNum}, callback=self.parse, formdata=formdata)