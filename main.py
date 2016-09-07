import vk
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
    post_id = IntegerField()

    class Meta:
        database = db


def download(pic, id, pic_id):
    resource = urlopen(pic)
    out = open('static\\img\\' + str(id) + '_' + 'pic' + '_' + str(pic_id) + '.jpg', 'wb')
    print(str(id) + '_' + 'pic' + '_' + str(pic_id))
    Pic.create(id=pic_id, post_id=id)
    out.write(resource.read())
    out.close()


def get_all_content(g_id):
    session = vk.Session()
    api = vk.API(session)

    group_id = '-' + g_id
    offset = 1
    while 1:
        try:
            group_posts = api.wall.get(owner_id=group_id, offset=offset, count=10)
            if len(group_posts) < 11:
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
                break
            else:
                print('else')
                offset += 10
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
        except Exception as err:
            print('Error')
            print(err)




def test_get(g_id):
    session = vk.Session()
    api = vk.API(session)
    offset = 1
    group_id = '-' + g_id
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


def url_get(g_id):
    session = vk.Session()
    api = vk.API(session)
    offset = 1
    group_id = '-' + g_id
    group_posts = api.wall.get(owner_id=group_id, offset=offset, count=5)

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
                    print(pic)
                    # download(pic, id, pic_id)
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


if __name__ == '__main__':
    get_all_content('101854455')
    print(1)
