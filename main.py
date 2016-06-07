import vk
from peewee import *
from urllib.request import urlopen

db = SqliteDatabase('content.db')


class Post(Model):
    text = TextField()
    pic_id = IntegerField()
    id = IntegerField()
    group_id = IntegerField()

    class Meta:
        database = db


class Comments(Model):
    text = TextField()
    post_id = IntegerField()

    class Meta:
        database = db


def download(pic, id):
    resource = urlopen(pic)
    out = open('static\\img\\' + str(id) + '_' + 'pic' + '.jpg', 'wb')
    out.write(resource.read())
    out.close()


def get_content(g_id):
    session = vk.Session()
    api = vk.API(session)

    group_id = '-' + g_id
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
        except:
            continue

