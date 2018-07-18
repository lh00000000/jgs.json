
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from pprint import pprint
from pydash import py_
from retrying import retry
import bisect
import csv
import frogress
import functools as ft
import heapq
import itertools as it
import math
import more_itertools as more
import operator as op
import random
import requests
import toolz as z
import json

import glob
import re


def reverse_list(l):
    reversed_list = l[:]
    reversed_list.reverse()
    return reversed_list


def normalize_art(raw_lines):
    def align_left(lines):
        def by_amt():
            def i_first_nonspace(line):
                return z.first(filter(lambda pair: pair[1] != " ", enumerate(line + "$")))[0]
            return min(map(i_first_nonspace, filter(len, lines)))
        return [line[by_amt():] for line in lines]

    def remove_signature(lines):
        return [line.replace("jgs", "   ") for line in lines]

    def strip_blank_lines(lines):

        def to_i():
            for i, line in reverse_list(list(enumerate(lines))):
                if line.strip() != line:
                    return i + 1
            return len(lines)

        def from_i():
            for i, line in enumerate(lines):
                if line.strip() != line:
                    return i
            return 0

        return lines[from_i():to_i()]

    return align_left(remove_signature(strip_blank_lines(raw_lines[1:])))


def metadata_record(raw_text):
    raw_lines = raw_text.splitlines()

    default_record = {
        "raw": raw_lines,
        "title": "",
        "date": "",
        "comment": "",
        "author": "jgs",
        "normalized": normalize_art(raw_lines)
    }

    if raw_text.startswith("-=["):
        first_line = raw_lines[0]

        title = re.match("^-=\[\ (.+)\ ]=-", first_line).group(1)
        date = first_line[-5:].strip()
        return {
            **default_record,
            "title": title,
            "date": date,
        }
    else:
        return default_record


def split_into_pieces(big_text):
    return big_text.replace("-=[", "<end>-=[").split("<end>")

json.dump({
    "url": "aquatic.html",
    "pieces": list(map(metadata_record, split_into_pieces(page_extract)))
}, open("aquatic.json", "w"))
