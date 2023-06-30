#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import requests
from lxml.html import fromstring
import argparse

requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

url_found = []

len_url_found = []

WARNING_METHOD = ["PATCH", "DELETE", "PUT"]


def check_allow_methods(uri):
    #print("\033[35m --\u251c Methods check \033[0m")
    req = requests.options(uri, verify=False)
    if "allow" in req.headers:
        for wm in WARNING_METHOD:
            if wm in req.headers["allow"]:
                print("\033[31m -\u251c The {} method for {} seems to be authorized !\033[0m".format(wm, uri))


def node_actions(url, type_, s):
    actions = ["revisions", "?_format=hal_json", "options"]
    print("\033[35m\u251c Check node actions \033[0m")
    for a in actions:
        if a == "options":
            for uf in url_found:
                check_allow_methods(uf)
        else:    
            for uf in url_found:
                uri = "{}/{}".format(uf, a) if not "?" in a else "{}{}".format(uf, a)
                req = s.get(uri, verify=False)
                if req.status_code not in [404, 403, 406] and len(req.content) != 174921 and "denied" not in req.text and len(req.content) not in len_url_found:
                    len_url_found.append(len(req.content))

                    tree = fromstring(req.content)
                    title = tree.findtext('.//title')
                    print("\033[32m{}\033[0m - [{}b] - {} :: \033[34m{}\033[0m".format(req.status_code, len(req.content), uri, title))
                sys.stdout.write(" {} \r".format(uri))
                sys.stdout.write("\033[K")


def main(url, type_, s, ranges):
    type_ = "taxonomy/term/" if type_ == "taxonomy" else "node/"
    print("\033[35m\u251c Check {} type \033[0m".format(type_))
    if ranges:
        range_1 = ranges.split("-")[0]
        range_2 = ranges.split("-")[1]
    else:
        range_1 = 0
        range_2 = 50
    for i in range(int(range_1),int(range_2)):
        uri = "{}{}{}".format(url, type_, i)
        req = s.get(uri, verify=False)
        if req.status_code not in [404] and len(req.content) != 174921 and len(req.content) not in len_url_found:
            url_found.append(uri)
            len_url_found.append(len(req.content))

            if len(req.content) != 0:
                tree = fromstring(req.content)
                title = tree.findtext('.//title')
            else:
                title = "None"
            print("\033[32m{}\033[0m - [{}b] - {} :: \033[34m{}\033[0m".format(req.status_code, len(req.content), uri, title))
        sys.stdout.write(" {} \r".format(uri))
        sys.stdout.write("\033[K")
    node_actions(url, type_, s)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument("-u", help="URL login to test \033[31m[required]\033[0m", dest='url')
    parser.add_argument("-r", help="range (Ex: 0-1000); Default: 0-1000", dest='ranges', required=False)
    parser.add_argument("-t", help="type of scan (taxonomy or node)", dest='type_', required=False)
    results = parser.parse_args()
                                     
    url = results.url
    ranges = results.ranges
    type_ = results.type_

    s = requests.Session()
    s.headers.update({'User-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; LCJB; rv:11.0) like Gecko'})


    main(url, type_, s, ranges)
