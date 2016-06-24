#-*- coding:utf-8 -*-

from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect

from .forms import CreateRepo, Login
from repos.models import Repository

from func import *
from settings import GITS_DIR, LOGIN_URL
from socket import gethostbyname, gethostname
from os import getcwd, path

import pygit2 as git

def homepage(request):
    temp = "index.html"
    context = {}

    try:
        login = request.session.get('login')
        if login == 1:
            repos = Repository.objects.all()
            context["repos"] = repos
    except:
        pass


    context = login_check(request, context)
    return render(request, temp, context)

def create(request):
    temp = "create.html"
    from settings import SSH_UID
    response = ""
    try:
        login = request.session.get('login')
        if login != 1:
            return HttpResponseRedirect(LOGIN_URL)
    except:
        return HttpResponseRedirect(LOGIN_URL)

    cr = CreateRepo(request.POST or None)
    if cr.is_valid():
        repoName = cr.cleaned_data['repositoryName']
        repoDesc = cr.cleaned_data['repositoryDesc']
        namecheck = name_check(repoName)
        if namecheck:
            newRepository, created = Repository.objects.get_or_create(name=namecheck,
                                                                      description=repoDesc)
            if created:
                newRepository.save()
                response = u"""Git Repository created.<br>
                    >> git remote add origin %s@%s:%s/gits/%s""" % (SSH_UID,
                                                                    gethostbyname(gethostname()),
                                                                    getcwd(),
                                                                    namecheck)
            else:
                response = "Repository name already exists."
        else:
            response = "Allowed chars: ['_', '-']"

    context = {'createf': cr, 'response': response}
    context = login_check(request, context)
    return render(request, temp, context)

def settings(request, repoName):
    temp = "settings.html"

    try:
        login = request.session.get('login')
        if login != 1:
            return HttpResponseRedirect(LOGIN_URL)
    except:
        return HttpResponseRedirect(LOGIN_URL)

    repoDesc = Repository.objects.get(name=repoName).description

    context = {"repoName":repoName, "repoDesc": repoDesc}
    context = login_check(request, context)
    return render(request, temp, context)

def repositoryG(request, repoName):
    temp = "main.html"
    try:
        login = request.session.get('login')
        if login != 1:
            return HttpResponseRedirect(LOGIN_URL)
    except:
        return HttpResponseRedirect(LOGIN_URL)

    context = {}
    try:
        repo = git.Repository(path.join(GITS_DIR, repoName))
        repoDesc = Repository.objects.get(name=repoName).description
        try:
            head = repo.revparse_single('HEAD')
        except:
            return HttpResponse("Repository is empty.")
        tree = head.tree
        ordered_tree = []
        tree_len = 0
        for tr in tree:
            if tr.type == 'tree':
                ordered_tree.insert(tree_len, tr)
                tree_len += 1
            else:
                ordered_tree.append(tr)


        context = {"tree": ordered_tree, "repoName": repoName, "repoDesc": repoDesc}
        context = login_check(request, context)
        return render(request, temp, context)
    except:
        return HttpResponse("Does not exists.")

def blobG(request, repoName, blob):
    temp = "blob.html"
    try:
        login = request.session.get('login')
        if login != 1:
            return HttpResponseRedirect(LOGIN_URL)
    except:
        return HttpResponseRedirect(LOGIN_URL)

    if blob:
        repo = git.Repository(path.join(GITS_DIR, repoName))
        repoDesc = Repository.objects.get(name=repoName).description
        head = repo.revparse_single('HEAD')
        tree = head.tree
        try:
            if tree[blob].type == 'tree':
                return HttpResponse("It's tree")
            else:
                oid = tree[blob].id
                object = repo[oid]
        except:
            return HttpResponse("Nothing.")

        #repoPath = blob.split("/")
        from collections import OrderedDict
        repoPath = OrderedDict()
        parent_path = ""
        for p in blob.split("/"):
            repoPath[p] = parent_path + p
            parent_path += p + "/"


        context = {"blob": object, "repoName": repoName, "repoDesc": repoDesc, "repoPath":repoPath, "name": blob}
        context = login_check(request, context)
        return render(request, temp, context)
    else:
        return HttpResponseRedirect("/%s"%repoName)

def treeG(request, repoName, treeName):
    temp = "tree.html"
    try:
        login = request.session.get('login')
        if login != 1:
            return HttpResponseRedirect(LOGIN_URL)
    except:
        return HttpResponseRedirect(LOGIN_URL)

    repo = git.Repository(path.join(GITS_DIR, repoName))
    repoDesc = Repository.objects.get(name=repoName).description
    head = repo.revparse_single('HEAD')
    tree = head.tree[treeName]
    tree = repo.get(tree.id)
    ordered_tree = []
    tree_len = 0
    for tr in tree:
        if tr.type == 'tree':
            ordered_tree.insert(tree_len, tr)
            tree_len += 1
        else:
            ordered_tree.append(tr)

    from collections import OrderedDict
    repoPath = OrderedDict()
    parent_path = ""
    for p in treeName.split("/"):
        repoPath[p] = parent_path + p
        parent_path += p + "/"

    context = {"tree":ordered_tree, "treeName":treeName, "repoName":repoName, "repoDesc":repoDesc, "repoPath":repoPath}
    context = login_check(request, context)
    return render(request, temp, context)

def login(request):
    temp = "login.html"
    loginform = Login(request.POST or None)

    if loginform.is_valid():
        username = loginform.cleaned_data['username']
        password = loginform.cleaned_data['password']
        from settings import LOGIN_PASSWORD, LOGIN_USERNAME
        if username == LOGIN_USERNAME and password == LOGIN_PASSWORD:
            request.session['login'] = 1
            request.session['user'] = username
            return HttpResponseRedirect('/')

    context = {"loginform": loginform}
    context = login_check(request, context)
    return render(request, temp, context)

def logout(request):
    try:
        login = request.session.get('login')
        if login != 1:
            return HttpResponseRedirect(LOGIN_URL)
        else:
            request.session['login'] = 0
            request.session['user'] = None
            return HttpResponseRedirect('/')
    except:
        return HttpResponseRedirect(LOGIN_URL)
