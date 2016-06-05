#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Imports

import re
from bottle import run, route, template, post, request, get, static_file
from main import Post, get_content

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


@route('/')
def index():
    get_content('-122615111')
    ids = []
    for post in Post.select():
        if post.id in ids:
            continue
        else:
            ids.append(post.id)
    return template('index.html', ids=['{}_pic.jpg'.format(id) for id in ids])

run(host='localhost', port=9999, debug=True)