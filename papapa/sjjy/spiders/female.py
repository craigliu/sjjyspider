import scrapy
import json, re

class FemaleSpider(scrapy.Spider):
    name = "female"
    allowed_domains = ["jiayuan.com"]

    SEARCH_TEMPLATE = {"sex":"f",
                       "key":"",
                       "stc":"1:{0},2:28.36,3:155.170,23:1",
                       "sn":"default",
                       "sv":"1",
                       "p":"1",
                       "f":"1",
                       "listStyle":"bigPhoto",
                       "pri_uid":"0",
                       "jsversion":"v5"};
    SEARCH_URL = "http://search.jiayuan.com/v2/search_v2.php"
    PROVINCE_CODES = ['11','12','13','14','15','21','22','23','31','32','33','34','35','36','37','41','42','43','44','45','46','50','51','52','53','54','61','62','63','64','65','71','81','82','98','99']

    MAX_PAGE_NUM = 10000

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

        for province in self.PROVINCE_CODES:
            formdata = self.SEARCH_TEMPLATE
            formdata["p"] = str(pageNum)
            searchProvinceTpl = formdata["stc"]
            formdata["stc"] = searchProvinceTpl.format(province)

            yield scrapy.FormRequest(self.SEARCH_URL, meta = {'cookiejar' : response.meta['cookiejar'], "page_num": pageNum, "form_data": formdata}, callback=self.parse, formdata=formdata)

    def parse(self, response):
        responseText = response.body_as_unicode()
        start = len("##jiayser##")
        end = len(responseText) - len("##jiayser##//")

        jsonresponse = json.loads(responseText[start:end])

        users = jsonresponse['userInfo']

        for user in users:
            #norm user icon
            userIcon = user['userIcon']
            p = re.compile(r'title=(\S*)')
            userIcon = p.findall(userIcon)
            user['userIcon'] = userIcon

            yield user

        if len(users) > 0:
            pageNum = response.meta['page_num']
            pageNum = pageNum + 1

            if pageNum <= self.MAX_PAGE_NUM:
                formdata = response.meta['form_data']
                formdata["p"] = str(pageNum)

                yield scrapy.FormRequest(self.SEARCH_URL, meta = {'cookiejar' : response.meta['cookiejar'], "page_num": pageNum, "form_data": formdata}, callback=self.parse, formdata=formdata)