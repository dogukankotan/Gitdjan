#-*- coding:utf-8 -*-

from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect

from .forms import CreateRepo, Login
from repos.models import Repository

from func import *
from socket import gethostbyname, gethostname
from os import getcwd

import pygit2 as git

def homepage(request):
    temp = "index.html"
    from settings import SSH_UID
    response = ""
    try:
        login = request.session.get('login')
        if login != 1:
            return HttpResponseRedirect('/login')
    except:
        return HttpResponseRedirect('/login')

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
                >> git remote add origin %s@%s:%s/gits/%s"""%(SSH_UID,
                                                              gethostbyname(gethostname()),
                                                              getcwd(),
                                                              namecheck)
            else:
                response = "Repository name already exists."
        else:
            response = "Allowed chars: ['_', '-']"


    repos = Repository.objects.all()

    context = {'createf': cr, 'response': response, "repos":repos}
    return render(request, temp, context)

def repositoryG(request, repoName):
    temp = "main.html"
    try:
        login = request.session.get('login')
        if login != 1:
            return HttpResponseRedirect('/login')
    except:
        return HttpResponseRedirect('/login')

    context = {}
    try:
        repo = git.Repository('gits/%s' % repoName)
        repoDesc = Repository.objects.get(name=repoName).description
        try:
            head = repo.revparse_single('HEAD')
        except:
            return HttpResponse("Repository is empty.")
        tree = head.tree

        context = {"tree": tree, "repoName": repoName, "repoDesc": repoDesc}
        return render(request, temp, context)
    except:
        return HttpResponse("Does not exists.")

def blobG(request, repoName, blob):
    temp = "blob.html"
    try:
        login = request.session.get('login')
        if login != 1:
            return HttpResponseRedirect('/login')
    except:
        return HttpResponseRedirect('/login')

    if blob:
        repo = git.Repository('gits/%s' % repoName)
        head = repo.revparse_single('HEAD')
        tree = head.tree
        if tree[blob].type == 'tree':
            return HttpResponse("It's tree")
        else:
            oid = tree[blob].id
            object = repo[oid]


        context = {"blob": object}
        return render(request, temp, context)
    else:
        return HttpResponseRedirect("/%s"%repoName)

def treeG(request, repoName, treeName):
    temp = "tree.html"
    try:
        login = request.session.get('login')
        if login != 1:
            return HttpResponseRedirect('/login')
    except:
        return HttpResponseRedirect('/login')

    repo = git.Repository('gits/%s' % repoName)
    head = repo.revparse_single('HEAD')
    tree = head.tree[treeName]
    tree = repo.get(tree.id)

    context = {"tree":tree, "treeName":treeName, "repo":repoName}
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
    return render(request, temp, context)

def logout(request):
    try:
        login = request.session.get('login')
        if login != 1:
            return HttpResponseRedirect('/login')
        else:
            request.session['login'] = 0
            request.session['user'] = None
            return HttpResponseRedirect('/login')
    except:
        return HttpResponseRedirect('/login')
