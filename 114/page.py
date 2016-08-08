#coding:utf-8
# https://addons.mozilla.org/en-us/firefox/addon/export-cookies/
import re
import mechanize
import cookielib
from lxml import etree
import HTMLParser
import time
import os

ROOT_DIR = os.getcwd()

class Pager(object):
    def __init__(self):
        br = mechanize.Browser()
        cookie = cookielib.MozillaCookieJar()
        cookie.load('%s/cookies.txt'%ROOT_DIR, ignore_discard=True, ignore_expires=True)

        #cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cookie)
        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        br.set_debug_http(False)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.1')]
        self.br = br
        self.cj = cookie
        self.base_url = "http://www.dianping.com"

    def list_page_links(self, url):
        # 构造返回值
        result = {}
        result["next_page"] = ""
        result["items"] = []

        print url
        response = self.br.open(url)
        body = response.read()
        html_tree = etree.HTML(body)
        # 当前页
        cur_page = html_tree.xpath("//div[@class='page']/a[@class='cur']")
        cur_page_num = int(cur_page[0].text)
        if cur_page_num < 50:
            next_page_num = cur_page_num + 1
            next_page_links = html_tree.xpath("//div[@class='page']/a[@data-ga-page='%d']"%next_page_num)
            next_page_url = "%s%s"%(self.base_url, next_page_links[0].get("href"))
            result["next_page"] = next_page_url
            # 匹配商铺链接
            shops_xpath = "//div[@id='shop-all-list']/ul/li/div[@class='txt']/div[@class='tit']/a[1]"
            shop_links = html_tree.xpath(shops_xpath)
            for shop_link in shop_links:
                result["items"].append("%s%s"%(self.base_url, shop_link.get("href")))
        else:
            print "........"
        return result

    def get_item_info(self, url):
        #url = "http://www.dianping.com/shop/65997732"
        result = {}
        result["title"] = ""
        result["phone"] = ""
        result["address"] = ""
        result["description"] = ""
        result["url"] = url

        dr = re.compile(r'<[^>]+>',re.S)
        parser = HTMLParser.HTMLParser()

        time.sleep(2)
        response = self.br.open(url)
        body = response.read()
        html_tree = etree.HTML(body)

        # 匹配标题
        shop_title_xpath = u"//div[@class='breadcrumb']/div[@class='inner']/span|//div[@class='breadcrumb']/strong|//div[@class='breadcrumb']/span"
        shop_titles = html_tree.xpath(shop_title_xpath)

        print url
        print shop_titles
        title = shop_titles[0].text
        result["title"] = title

        # 匹配地址
        shop_address_xpath = u"//div[@class='brief-info']/div[@class='address']|//div[@class='shop-info']/div[@class='shop-addr']/span|//div[@itemprop='street-address']"
        shop_addresses = html_tree.xpath(shop_address_xpath)
        address_str = etree.tostring(shop_addresses[0])
        address_str = dr.sub('', address_str)
        result["address"] = parser.unescape(address_str)

        # 匹配电话
        shop_phone_xpath = u"//div[@class='book']/div[@class='phone']/span|//div[@class='shop-info']/div[@class='shopinfor']/p/span[1]|//span[@itemprop='tel']"
        shop_phones = html_tree.xpath(shop_phone_xpath)
        if shop_phones:
            shop_phone = shop_phones[0].text
            result["phone"] = shop_phone

        # 匹配简介
        shop_desc_xpath = u"//div[@class='mod-wrap']/div[@id='info']/ul/li[2]|//div[@class='con J_showWarp']/div[@class='block_all']/div[2]/span"
        shop_descs = html_tree.xpath(shop_desc_xpath)
        if shop_descs:
            shop_desc_str = etree.tostring(shop_descs[0])
            shop_desc_str = dr.sub('', shop_desc_str)
            result["description"] = parser.unescape(shop_desc_str)

        return result



