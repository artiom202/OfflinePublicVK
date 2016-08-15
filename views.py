#!/usr/bin/env python
# -*- coding: utf-8 -*-


#Imports

import time
from bottle import run, route, template, post, request, get, static_file, redirect
from main import Post, test_get, Comments

#/Imports

# Static Routes


@get('/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='static/js')


@get('/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='static/css')


@get('/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='static/img')


@get('/<filename:re:.*\.(eot|ttf|woff|svg)>')
def fonts(filename):
    return static_file(filename, root='static/fonts')


@get('/')
def index():
    return template('templates/index.html')


@route('/<g_id>')
def pabl(g_id):
    test_get(g_id)
    ids = []
    for post in Post.select().where(Post.group_id == g_id):
        if post.id in ids:
            continue
        else:
            ids.append(post.id)
    return template('templates/pabl.html', ids=ids, Comments=Comments)


run(host='localhost', port=9999, debug=True)

