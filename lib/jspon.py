#!python

from simplejson import dumps, loads
import re

def from_jspon(string, **args):
    return loads(string)

# re.match(r'^(.*?(\[.*\])+)\.(.*)', 'foo[hello[foo].bar].bar').groups()

def parse_jspon(string):
    ids = {}
    refs = []

    def traverse(v):
        if type(v) == list:
            for i in xrange(len(v)):
                value = v[i]

                if type(value) == list:
                    traverse(value)
                    continue

                if type(value) == dict:
                    ref = value.get('$ref')
                    if ref:
                        refs.append((i, v))
                
                traverse(value)

        elif type(v) == dict:
            id = v.get('id')
            if id:
                ids[id] = v

            for item in v:
                value = v[item]

                if type(value) == list:
                    traverse(value)
                    continue
                
                if type(value) == dict:
                    ref = value.get('$ref')
                    if ref:
                        refs.append((item, v))
                
                traverse(value)
    obj = loads(string)
    traverse(obj)
    fill_in_refs(ids, refs)
    return obj

def fill_in_refs(ids, refs):
    for key, value in refs:
        id = value[key]['$ref']
        value[key] = ids[id]
