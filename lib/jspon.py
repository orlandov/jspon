#!python

from simplejson import dumps, loads
import re

def from_jspon(string, **args):
    return loads(string)

# re.match(r'^(.*?(\[.*\])+)\.(.*)', 'foo[hello[foo].bar].bar').groups()

def parse_jspon(string):
    """
    Parse a JSON string with embedded JSPON references into a structure with
    the appropriate references filled in.
    """

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

    def fill_in_refs(ids, refs):
        for key, value in refs:
            refval = value[key]['$ref']
            if refval == '$':
                value[key] = root
                continue

            try:
                value[key] = ids[refval]
            except KeyError:
                raise RuntimeError("Invalid reference: %s" % (value[key]['$ref'],))


    obj = loads(string)
    ids = {}
    refs = []
    root = obj

    # Walk the parsed structure and record occurances of "id" and "$ref"
    traverse(obj)

    # Iterate over the list of references, replacing them with real
    # references in their containing structure.
    fill_in_refs(ids, refs)
    return obj

