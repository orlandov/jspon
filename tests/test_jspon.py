#!python

from unittest import TestCase
from jspon import parse_jspon
from simplejson import loads, dumps

class TestRootReference(TestCase):
    def test_root(self):
        string = """{ "id": "1", "foo": { "$ref": "$" }, "baz": "42"}"""
        obj = parse_jspon(string)
        self.assertEqual(obj['foo']['baz'], obj['baz'])

class TestReferenceById(TestCase):
    def test_simple(self):
        string = """{ "foo": "bar" }"""
        obj = parse_jspon(string)

    def test_dict_reference(self):
        string = """{ "id": "1", "foo": { "$ref": "1" }, "baz": "42"}"""
        obj = parse_jspon(string)
        self.assertEqual(obj['foo']['baz'], obj['baz'])

    def test_list_reference(self):
        string = """
        {
            "id": "1",
            "foo": [
                { "$ref": "1" },
                { "$ref": "1" }
            ],
            "baz": "42"
        }"""

        obj = parse_jspon(string)
        self.assertEqual(obj['foo'][0]['baz'], obj['foo'][1]['baz'])

    def test_bi_directional(self):
        string = """
        [
            {
                "id": "1",
                "bar": {
                    "$ref": "2"
                },
                "name": "item 1"
            },
            {
                "id": "2",
                "bar": {
                    "$ref": "1"
                },
                "name": "item 2"
            }
        ]"""

        obj = parse_jspon(string)
        self.assertEqual(obj[0]['bar']['name'], "item 2")
        self.assertEqual(obj[1]['bar']['name'], "item 1")

class TestInvalidReference(TestCase):
    def test_non_existant_ref(self):
        string = """{ "id": "1", "foo": { "$ref": "2" }, "baz": "42"}"""
        self.assertRaises(RuntimeError, parse_jspon, string)

    def test_non_existant_ref2(self):
        string = """{ "foo": { "$ref": "1" }, "baz": "42"}"""
        self.assertRaises(RuntimeError, parse_jspon, string)

