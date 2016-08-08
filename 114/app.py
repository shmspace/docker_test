#!/usr/bin/env python
#coding:utf-8

import settings
import page

print settings.dianping_url_map

shop_info = []

dianping_pager = page.Pager()
result = dianping_pager.list_page_links(settings.dianping_url_map['waiyu'])
print result["next_page"]

for item in result["items"]:
    item_info = dianping_pager.get_item_info(item)
    shop_info.append(item_info)
    print item_info

while result["next_page"] != "":
    result = dianping_pager.list_page_links(result["next_page"])
    for item in result["items"]:
        item_info = dianping_pager.get_item_info(item)
        shop_info.append(item_info)
        print item_info






