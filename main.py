#!/usr/bin/env python
# -*- coding: utf-8 -*-
import vk
from peewee import *
#from urllib.request import urlopen    # Для работы с веб страницами

db = SqliteDatabase('content.db')    # Подключаем базу данных и определяем модели таблиц


class Post(Model):
    '''Класс поста на стене'''

    text = TextField()
    id = IntegerField()
    group_id = IntegerField()

    class Meta:
        database = db


class Comments(Model):
    '''Класс комментариев под постом'''

    text = TextField()
    post_id = IntegerField()

    class Meta:
        database = db


class Pic(Model):
    '''Класс картинки прикрепленной к посту'''

    id = IntegerField()
    post_id = IntegerField()
    url = TextField()

    class Meta:
        database = db

class Doc(Model):
    '''Класс документа прикрепленного к посту'''

    id = IntegerField()
    post_id = IntegerField()
    url = TextField()
    name = TextField()

    class Meta:
        database = db

class Video(Model):
    '''Класс видео прикрепленного к посту'''

    id = IntegerField()
    post_id = IntegerField()
    platform = TextField()
    name = TextField()

    class Meta:
        database = db

class Audio(Model):
    '''Класс музыкального трека прикрепленного к посту'''

    id = IntegerField()
    post_id = IntegerField()
    artist = TextField()
    title = TextField()
    url = TextField()

    class Meta:
        database = db

class Link(Model):
    '''Класс ссылки прикрепленной к посту'''

    post_id = IntegerField()
    url = TextField()
    title = TextField()

    class Meta:
        database = db

'''def download(pic, id, pic_id):
    Функция для загрузки фото по ссылке
    
    resource = urlopen(pic)
    # Windows
	# out = open('static\\img\\' + str(id) + '_' + 'pic' + '_' + str(pic_id) + '.jpg', 'wb')
    # Linux
    out = open('static/img/' + str(id) + '_' + 'pic' + '_' + str(pic_id) + '.jpg', 'wb')
    print(str(id) + '_' + 'pic' + '_' + str(pic_id))
    Pic.create(id=pic_id, post_id=id)
    out.write(resource.read())
    out.close()
'''

def get_picture(attachment,post_pic_id):
    '''Функция записывающая данные о картинке в бд'''

    pic = attachment.get('photo').get('src_big')
    pic_id = attachment.get('photo').get('pid')
    Pic.create(id=pic_id, post_id=post_pic_id, url=pic)    # Создаем запись о картинке в бд


def get_document(attachment,post_doc_id):
    '''Функция записывающая данные о документе в бд'''

    doc = attachment.get('doc').get('url')
    doc_id = attachment.get('doc').get('did')
    doc_name = attachment.get('doc').get('title')
    Doc.create(id=doc_id, post_id=post_doc_id, url=doc, name=doc_name)    # Создаем запись о документе в бд

def get_video(attachment,post_vid_id):
    '''Функция записывающая данные о видео в бд'''

    video_platform = attachment.get('video').get('platform')
    vid_id = attachment.get('video').get('vid')
    vid_name = attachment.get('video').get('title')
    Video.create(id=vid_id, post_id=post_vid_id, platform=video_platform, name=vid_name)    # Создаем запись о видео в бд

def get_audio(attachment,post_audio_id):
    '''Функция записывающая данные о музыкальном треке в бд'''

    audio_url = attachment.get('audio').get('url')
    audio_id = attachment.get('audio').get('aid')
    audio_artist = attachment.get('audio').get('artist')
    audio_title = attachment.get('audio').get('title')
    Audio.create(id=audio_id, post_id=post_audio_id, artist=audio_artist, title=audio_title, url=audio_url)    # Создаем запись о музыкальном треке в бд

def get_link(attachment,post_link_id):
    '''Функция записывающая данные о прикрепленной ссылке в бд'''

    link = attachment.get('link').get('url')
    link_title = attachment.get('link').get('title')
    Link.create(post_id=post_link_id, url=link, title=link_title)    # Создаем запись о ссылке в бд


def get_post(group_post,group_id,post_id,post_comments):
    '''Функция записывающая данные о посте в бд'''

    text = group_post.get('text')
    for attachment in group_post.get('attachments'):
        if attachment.get('type') == 'photo': 
            get_picture(attachment,post_id)
        elif (attachment.get('type') == 'doc'):
            get_document(attachment,post_id)
        elif (attachment.get('type') == 'link'):
            get_link(attachment,post_id)
        elif (attachment.get('type') == 'video'):
            get_video(attachment,post_id)
        elif (attachment.get('type') == 'audio'):
            get_audio(attachment,post_id)

    for i in range(len(post_comments) - 1):
        comment = post_comments[1:len(post_comments)][i]
        if comment.get('likes').get('count') > 1:
            if not 'https://vk.com' in comment.get('text'):
                if not '[id' in comment.get('text'):
                    Comments.create(id=comment.get('cid'),text=comment.get('text'), post_id=post_id)    # Создаем запись о комментарие в бд
    Post.create(text=text, id=post_id, group_id=group_id)    # Создаём запись о посте в бд


def get_all_content(g_id):
    '''Основная функция для загрузки картинок и комментов'''

    # Определяем сессию вк
    session = vk.Session()
    api = vk.API(session)

    group_id = g_id
    group_id_negative = int('-' + str(g_id))
    offset = 1
    try:
        group_posts = api.wall.get(owner_id=group_id_negative, offset=offset, count=10)    # Получаем посты из группы
    except Exception as err:
        group_posts = []
        print('Error no wall')
        print(err)    
    if len(group_posts) > 0:
        end=False    # Условие работы главного цикла

        # Главный цикл
        while end!=True:
            try:
                if len(group_posts)<10:    
                    for group_post in group_posts[1:len(group_posts)]:
                        try:
                            post_id = group_post.get('id')
                            post_comments = api.wall.getComments(owner_id=group_id_negative, post_id=post_id, need_likes=True)
                            get_post(group_post,group_id,post_id,post_comments)
                        except Exception as err:
                            print(err)
                            print('Error get post')
                    end=True
                else:
                    print('else')
                    offset += 10
                    for group_post in group_posts[1:len(group_posts)]:
                        try:
                            post_id = group_post.get('id')
                            post_comments = api.wall.getComments(owner_id=group_id_negative, post_id=post_id, need_likes=True)
                            get_post(group_post,group_id,post_id,post_comments)
                        except Exception as err:
                            print(err)
                            print('Error get post')
                    try:
                        group_posts = api.wall.get(owner_id=group_id_negative, offset=offset, count=10)    #Получаем следующие посты из группы
                    except Exception as err:
                        print('Error get new wall')
                        print(err)
                        end=True
            except Exception as err:
                print('Error all')
                print(err)


def test_content(g_id):
    '''Функция берущая первые 10 постов'''

    # Определяем сессию вк
    session = vk.Session()
    api = vk.API(session)

    group_id = g_id
    group_id_negative = int('-' + str(g_id))
    offset = 0
    try:
        group_posts = api.wall.get(owner_id=group_id_negative, offset=offset, count=10)
    except Exception as err:
        group_posts = []
        print('Error no wall')
        print(err)
    if len(group_posts) > 0:
        for group_post in group_posts[1:len(group_posts)]:
            try:
                post_id = group_post.get('id')
                post_comments = api.wall.getComments(owner_id=group_id_negative, post_id=post_id, need_likes=True)
                get_post(group_post,group_id,post_id,post_comments)
            except Exception as err:
                print(err)
                print('Error get post')


# Конструкция для дебага
if __name__ == '__main__':
    get_all_content('101854455')
    print(1)
