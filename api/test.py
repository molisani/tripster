#!/usr/bin/env python

from api import *
 
data = {"username":"molisani", "items":["item1", "item2", "item3", {"subitem1":"a", "subitem2":"b"}]}

data['tables'] = [x for y in execute_query("SHOW TABLES") for x in y]

data['fields'] = str(post)

export_json(data)
