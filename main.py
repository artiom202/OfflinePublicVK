import vk # для работы с  вк
from peewee import * # для работы с бд
from urllib.request import urlopen # для работы с веб страницами

#Подклчаем базу данных и определяем модели таблиц
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
    url = TextField()

    class Meta:
        database = db


# Функция для загрузки фото по ссылке
def download(pic, id, pic_id):
    resource = urlopen(pic)
    # Windows
	# out = open('static\\img\\' + str(id) + '_' + 'pic' + '_' + str(pic_id) + '.jpg', 'wb')
    # Linux
    out = open('static/img/' + str(id) + '_' + 'pic' + '_' + str(pic_id) + '.jpg', 'wb')
    print(str(id) + '_' + 'pic' + '_' + str(pic_id))
    Pic.create(id=pic_id, post_id=id)
    out.write(resource.read())
    out.close()


# Основная функция для загрузки картинок и коментов
def get_all_content(g_id):
    # определяем сессию вк
    session = vk.Session()
    api = vk.API(session)

    group_id = '-' + g_id
    offset = 1
    # главный цикл
    while 1:
        try:
            
            group_posts = api.wall.get(owner_id=group_id, offset=offset, count=10)
            # для того чтобы загрузить все посты из групы мы проверяем меньше ли их чем 10
            if len(group_posts) < 11:
                # получаем посты из группы, и вытаскиваем из json ответа: 
                for group_post in group_posts[1:len(group_posts)]:
                    try:
                        text = group_post.get('text')
                        id = group_post.get('id')
                        if id in [post.id for post in Post.select()]:
                            continue
                        for attachment in group_post.get('attachments'):

                            if attachment.get('type') == 'photo':
                                # картинки 
                                pic = attachment.get('photo').get('src_big')
                                pic_id = attachment.get('photo').get('pid')
                                Pic.create(id=pic_id, post_id=id, url=pic)
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
                                        # коменты
                                        Comments.create(text=comment.get('text'), post_id=id)
                                    else:
                                        continue
                        # Создаём новый пост в бд
                        Post.create(text=text, id=id, group_id=g_id)
                    except Exception as err:
                        print(err)
                # если да, то прерываем главный цикл 
                break
            # если нет, то продолжаем выгружать контент
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
                                Pic.create(id=pic_id, post_id=id, url=pic)
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

# Конструкция для дебага
if __name__ == '__main__':
    get_all_content('101854455')
    print(1)
