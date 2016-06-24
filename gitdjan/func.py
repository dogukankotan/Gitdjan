#-*- coding:utf-8 -*-

from re import escape

def login_check(req, cont):
    try:
        lCheck = req.session.get('login')
    except:
        lCheck = 0

    cont['login'] = lCheck
    return cont

def name_check(name):
    namex = escape(name)
    namex = namex.replace("\\-", "-")
    namex = namex.replace("\\_", "_")
    namex = namex.replace("\\ ", "-")
    name = name.replace(" ", "-")

    if name == namex:
        return name.lower()
    else:
        return False

