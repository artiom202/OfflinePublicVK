import vk
import os
from peewee import *
from urllib.request import urlopen

db = SqliteDatabase('content.db')


class Post(Model):
    text = TextField()
    id = IntegerField()
    group_id = IntegerField()

    class Meta:
        database = db


class Comments(Model):
    text = TextField()
    post_id = IntegerField()

    class Meta:
        database = db


class Pic(Model):
    id = IntegerField()

    class Meta:
        database = db


def download(pic, id, pic_id):
    resource = urlopen(pic)
    if not os.access(os.path.join("static","img",""),os.F_OK):
        os.makedirs(os.path.join("static","img",""))
    out = open(os.path.join("static","img","") + str(id) + '_' + 'pic' + '.jpg', 'wb')
    out.write(resource.read())
    out.close()
    Pic.create(id=pic_id)

def get_all_content(g_id):
    session = vk.Session()
    api = vk.API(session)

    group_id = '-' + g_id
    ofset = 1
    while 1:
        group_posts = api.wall.get(owner_id=group_id, offset=ofset, count=50)
        if len(group_posts) < 11:
            text = group_posts.get('text')
            id = group_posts.get('id')
            pic = group_posts.get('attachments')[0].get('photo').get('src_big')
            if id in [post.id for post in Post.select()]:
                continue
            else:
                download(pic, id)
                post_comments = api.wall.getComments(owner_id=group_id, post_id=id, need_likes=True)
                for i in range(len(post_comments)-1):
                    comment = post_comments[1:len(post_comments)][i]
                    if comment.get('likes').get('count') > 1:
                        if 'https://vk.com' in comment.get('text'):
                            continue
                        else:
                            if not '[id' in comment.get('text'):
                                Comments.create(text=comment.get('text'), post_id=id)
                            else:
                                continue
                Post.create(text=text, pic_id=id, id=id, group_id=g_id)
            sleep(30)
            break
        else:
            for group_post in group_posts[1:len(group_posts)]:
                text = group_post.get('text')
                id = group_post.get('id')
                pic = group_post.get('attachments')[0].get('photo').get('src_big')
                if id in [post.id for post in Post.select()]:
                    continue
                else:
                    download(pic, id)
                    post_comments = api.wall.getComments(owner_id=group_id, post_id=id, need_likes=True)
                    for i in range(len(post_comments)-1):
                        comment = post_comments[1:len(post_comments)][i]
                        if comment.get('likes').get('count') > 1:
                            if 'https://vk.com' in comment.get('text'):
                                continue
                            else:
                                if not '[id' in comment.get('text'):
                                    Comments.create(text=comment.get('text'), post_id=id)
                                else:
                                    continue

                    Post.create(text=text, pic_id=id, id=id, group_id=g_id)

                sleep(30)
                continue
            print('iterration++')
        ofset += 10
        

def get_content(g_id):
    session = vk.Session()
    api = vk.API(session)

    group_id = int('-' + str(g_id))
    group_posts = api.wall.get(owner_id=group_id, offset=1, count=50)
    for group_post in group_posts[1:len(group_posts)]:
        try:
            text = group_post.get('text')
            id = group_post.get('id')
            pic = group_post.get('attachments')[0].get('photo').get('src_big')
            if id in [post.id for post in Post.select()]:
                continue
            else:
                download(pic, id)
                post_comments = api.wall.getComments(owner_id=group_id, post_id=id, need_likes=True)
                for i in range(len(post_comments)-1):
                    comment = post_comments[1:len(post_comments)][i]
                    if comment.get('likes').get('count') > 1:
                        if 'https://vk.com' in comment.get('text'):
                            continue
                        else:
                            if not '[id' in comment.get('text'):
                                comment = Comments.create(text=comment.get('text'), post_id=id)
                            else:
                                continue

                post = Post.create(text=text, pic_id=id, id=id, group_id=g_id)
        except Except as error:
            print(error)
            continue


def test_get(g_id):
    session = vk.Session()
    api = vk.API(session)
    offset = 1
    group_id = int('-' + str(g_id))
    group_posts = api.wall.get(owner_id=group_id, offset=offset, count=50)

    for group_post in group_posts[1:len(group_posts)]:
        try:
            text = group_post.get('text')
            id = group_post.get('id')
            if id in [post.id for post in Post.select()]:
                continue
            for attachment in group_post.get('attachments'):

                if attachment.get('type') == 'photo':
                    pic = attachment.get('photo').get('src_big')
                    pic_id = attachment.get('photo').get('pid')
                    download(pic, id, pic_id)
                else:
                    continue
            post_comments = api.wall.getComments(owner_id=group_id, post_id=id, need_likes=True)
            for i in range(len(post_comments) - 1):
                comment = post_comments[1:len(post_comments)][i]
                if comment.get('likes').get('count') > 1:
                    if 'https://vk.com' in comment.get('text'):
                        continue
                    else:
                        if not '[id' in comment.get('text'):
                            Comments.create(text=comment.get('text'), post_id=id)
                        else:
                            continue

            Post.create(text=text, id=id, group_id=g_id)
        except Exception as err:
            print(err)
            continue
