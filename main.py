import vk
from peewee import *
from urllib.request import urlopen

db = SqliteDatabase('content.db')


class Post(Model):
    text = TextField()
    pic_id = IntegerField()
    id = IntegerField()

    class Meta:
        database = db


def download(pic, id, is_comment_pic):
    resource = urlopen(pic)
    if is_comment_pic:
        out = open('static\\img\\' + str(id) + '_' + 'comment' + '_' + 'pic' + '.jpg', 'wb')
    else:
        out = open('static\\img\\' + str(id) + '_' + 'pic' + '.jpg', 'wb')
    out.write(resource.read())
    out.close()


def get_content(group_id):
    session = vk.Session()
    api = vk.API(session)

    group_id = group_id
    group_posts = api.wall.get(owner_id=group_id, offset=1, count=30)
    for group_post in group_posts[1:len(group_posts)]:
        text = group_post.get('text')
        id = group_post.get('id')
        pic = group_post.get('attachments')[0].get('photo').get('src_big')
        download(pic, id, False)
        #post_comments = api.wall.getComments(owner_id=group_id, post_id=id, need_likes=True)
        post = Post.create(text=text, pic_id=id, id=id)

        """
        for i in range(len(post_comments)-1):
            comment = post_comments[1:len(post_comments)][i]
            if comment.get('likes').get('count') > 1:
                if 'https://vk.com' in comment.get('text'):
                    download(comment.get('text'), id, True)
                else:
                    comment_text = comment.get('text')
        """

