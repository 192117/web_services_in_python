import os
import re
import time

from bs4 import BeautifulSoup

def parse(path_to_file):
    with open(path_to_file, "r", encoding="utf-8") as html:
        soup = BeautifulSoup(html, "html.parser")
        content = soup.find("div", id="bodyContent")
        return [parse_img(content), parse_headers(content), parse_link(content), parse_list(content)]


def parse_img(content):
    img_from_d = content.find_all("img")
    imgs = 0
    for i in img_from_d:
        if i.has_attr('width') and int(i["width"]) >= 200:
            imgs += 1
    return imgs


def parse_headers(content):
    heads = ["h1", "h2", "h3", "h4", "h5", "h6"]
    headers = 0
    for head in heads:
        header = content.find_all(head)
        letters = ["E", "T", "C"]
        for i in header:
            if i.text[0] in letters:
                headers += 1
    return headers


def parse_link(content):
    aparents = [0]
    list_a = content.find_all('a')
    h = list_a[0].parent
    i = 0
    for a in list_a:
        if a.parent is h and (i == 0 or a.previousSibling.name == 'a' or a.previousSibling.previousSibling.name == 'a'):
            aparents[i] += 1
            h = a.parent
        else:
            aparents.append(1)
            i += 1
            h = a.parent
    return max(aparents)


def parse_list(content):
    lists = [list_ for list_ in content.find_all(["ol", "ul"]) if list_.find_parent(["ol", "ul"]) is None]
    return len(lists)

