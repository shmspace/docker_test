#coding=utf-8

import re
import mechanize
import cookielib
from lxml import etree
import HTMLParser

br = mechanize.Browser()  
cj = cookielib.LWPCookieJar()  
br.set_cookiejar(cj)  
br.set_handle_equiv(True)  
br.set_handle_gzip(True)  
br.set_handle_redirect(True)  
br.set_handle_referer(True)  
br.set_handle_robots(False)  
  
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)  
br.set_debug_http(False)  
  
br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:15.0) Gecko/20100101 Firefox/15.0.1')]  
  
response1 = br.open('http://www.dianping.com/search/category/1/75/g2872')  

title = br.title()
url = response1.geturl()
info = response1.info()  # headers
body = response1.read()  # body

print "================="
print title
print url
print info

print "================="

tree = etree.HTML(body)
links = tree.xpath(u"//a[@class='PageLink']")

print links[0].tag
print links[0].get("href")

shop_xpath = u"//div[@class='tit']/a[@data-hippo-type='shop']"
shops = tree.xpath(shop_xpath)
print shops[0].get("href")

shop_link = shops[0].get("href")
response2 = br.open("http://www.dianping.com"+shop_link)

body = response2.read()
tree_shop = etree.HTML(body)

shop_title_xpath = u"//div[@class='shop-name']/h2"
shop_titles = tree_shop.xpath(shop_title_xpath)

title = shop_titles[0].text
print title.encode("utf-8")

shop_address_xpath = u"//div[@class='brief-info']/div[@class='address']"
shop_addresses = tree_shop.xpath(shop_address_xpath)

address_str = etree.tostring(shop_addresses[0])

dr = re.compile(r'<[^>]+>',re.S)
dd = dr.sub('', address_str)

parser = HTMLParser.HTMLParser()
print parser.unescape(dd)
