# Моя реализация не проходит по времени. Можно ускорить засчет использования set() вместо list() и соответственно
# изменения немного логики.
import os
import re
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


def articale_parse(path, page):
    with open(os.path.join(path, page), encoding="utf-8") as file:
        total_wiki = []
        for i in os.walk(path):
            for lin in i[2]:
                total_wiki.append(lin)
        soup = BeautifulSoup(file, "html.parser")
        links = []
        for i in soup.find_all("a", {"href": re.compile("\/wiki\/[\\w]+")}):
            if "Wikipedia" not in i["href"]:
                if i["href"].split("/")[-1] in total_wiki:
                    if i["href"].split("/")[-1] != page:
                        links.append(i["href"].split("/")[-1])
    return links


def build_bridge(path, start_page, end_page):
    """возвращает список страниц, по которым можно перейти по ссылкам со start_page на
    end_page, начальная и конечная страницы включаются в результирующий список"""

    def bsf(start_url):
        answer = dict()
        visited = []
        queue = []
        queue.append(start_url)
        while queue:
            url = queue.pop(0)
            links = articale_parse(path, url)
            answer[url] = links
            if end_page in links:
                visited.append(url)
                break
            for link in links:
                if link not in visited:
                    queue.append(link)
            visited.append(url)
        return answer

    result = bsf(start_page)

    def search(data):
        answer1 = []
        page = end_page
        while page != start_page:
            for key in data:
                if page in data[key]:
                    answer1.append(key)
                    page = key
                    break
        return answer1[::-1]

    data_list = search(result)
    data_list.append(end_page)

    return data_list


def get_statistics(path, start_page, end_page):
    """собирает статистику со страниц, возвращает словарь, где ключ - название страницы,
    значение - список со статистикой страницы"""
    statistic = dict()
    pages = build_bridge(path, start_page, end_page)
    for page in pages:
        statistic[page] = parse(path + page)
    return statistic

# Решение второй части от преподавателей.
# def get_statistics(path, start_page, end_page):
#     """собирает статистику со страниц, возвращает словарь, где ключ - название страницы,
#     значение - список со статистикой страницы"""
#     pages = build_bridge(path, start_page, end_page)
#     statistic = {}
#
#     for page in pages:
#         statistic[page] = parse(os.path.join(path, page))
#
#     return statistic
#
#
# def get_links(path, page):
#     """возвращает множество названий страниц, ссылки на которые содержатся в файле page"""
#
#     with open(os.path.join(path, page), encoding="utf-8") as file:
#         links = set(re.findall(r"(?<=/wiki/)[\w()]+", file.read()))
#         if page in links:
#             links.remove(page)
#     return links
#
#
# def get_backlinks(path, end_page, unchecked_pages, checked_pages, backlinks):
#     """возвращает словарь обратных ссылок (ключ - страница, значение - страница
#     с которой возможен переход по ссылке на страницу, указанную в ключе)"""
#
#     if end_page in checked_pages or not checked_pages:
#         return backlinks
#
#     new_checked_pages = set()
#
#     for checked_page in checked_pages:
#         unchecked_pages.remove(checked_page)
#         linked_pages = get_links(path, checked_page) & unchecked_pages
#
#         for linked_page in linked_pages:
#             backlinks[linked_page] = backlinks.get(linked_page, checked_page)
#             new_checked_pages.add(linked_page)
#
#     checked_pages = new_checked_pages & unchecked_pages
#
#     return get_backlinks(path, end_page, unchecked_pages, checked_pages, backlinks)
#
#
# def build_bridge(path, start_page, end_page):
#     """возвращает список страниц, по которым можно перейти по ссылкам со start_page на
#     end_page, начальная и конечная страницы включаются в результирующий список"""
#
#     backlinks = \
#         get_backlinks(path, end_page, set(os.listdir(path)), {start_page, }, dict())
#
#     current_page, bridge = end_page, [end_page]
#
#     while current_page != start_page:
#         current_page = backlinks.get(current_page)
#         bridge.append(current_page)
#
#     return bridge[::-1]