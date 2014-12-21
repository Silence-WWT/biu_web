# -*- coding: utf-8 -*-
from random import randint, seed, random, randrange

from flask import current_app
from flask.ext.login import UserMixin
from flask.ext.scrypt import generate_random_salt, generate_password_hash, check_password_hash

from app import db
from utils import time_now

seed()


class UnifiedUser(db.Model):
    __tablename__ = 'unified_users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    identity = db.Column(db.String(64), nullable=False)
    created = db.Column(db.Integer, default=time_now, nullable=False)

    @staticmethod
    def get_unified_user(user_id, identity=''):
        if not user_id:
            unified_user = UnifiedUser.query.filter_by(identity=identity).limit(1).first()
            if not unified_user:
                unified_user = UnifiedUser(user_id='', identity=identity)
                db.session.add(unified_user)
                db.session.commit()
        else:
            user = User.query.get(user_id)
            # TODO: user may be None
            unified_user = UnifiedUser.query.filter_by(user_id=user_id).limit(1).first()
            if not unified_user:
                unified_user = UnifiedUser(user_id=user_id, identity=user.identity)
                db.session.add(unified_user)
                db.session.commit()
        return unified_user

    @staticmethod
    def synchronize(user_id, identity):
        unified_users = UnifiedUser.query.filter_by(user_id='', identity=identity)
        for unified_user in unified_users:
            unified_user.user_id = user_id


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.Unicode(10), default=u'', nullable=False)
    password_hash = db.Column('password', db.String(128), nullable=False)
    salt = db.Column(db.String(128), nullable=False)
    sex = db.Column(db.SmallInteger, default=2, nullable=False)
    created = db.Column(db.Integer, default=time_now, nullable=False)
    email = db.Column(db.String(64), nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False, nullable=False)
    identity = db.Column(db.String(64), nullable=False)
    golds = db.Column(db.Integer, default=0, nullable=False)
    avatar = db.Column(db.String(128), default='', nullable=False)
    signature = db.Column(db.Unicode(30), default=u'', nullable=False)
    push = db.Column(db.Boolean, default=True, nullable=False)
    disturb = db.Column(db.Boolean, default=True, nullable=False)
    # Android 0, iOS 1
    device = db.Column(db.SmallInteger, default=0, nullable=False)

    @staticmethod
    def get_random_id():
        while 1:
            random_id = randint(10000000, 99999999)
            if not User.query.get(random_id):
                return random_id

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.salt = generate_random_salt()
        self.password_hash = generate_password_hash(password, self.salt)

    def verify_password(self, password):
        return check_password_hash(password, self.password_hash, self.salt)

    def update_identity_device(self, identity, device):
        if identity and identity != self.identity:
            self.identity = identity
        if device != self.device:
            self.device = device

    def get_self_info_dict(self, is_self=True):
        user_dict = {
            'user_id': self.id,
            'nickname': self.nickname,
            'golds': self.golds,
            'avatar': self.get_avatar(),
            'signature': self.signature,
            'sex': self.sex,
            'followings_count': Fan.query.filter_by(user_id=self.id, is_deleted=False).count(),
            'followers_count': Fan.query.filter_by(idol_id=self.id, is_deleted=False).count(),
        }
        if is_self:
            user_dict['identity'] = self.identity
            user_dict['email'] = self.email
            user_dict['push'] = self.push
            user_dict['disturb'] = self.disturb
        return user_dict

    def get_brief_info_dict(self):
        return {
            'user_id': self.id,
            'nickname': self.nickname,
            'avatar': self.get_avatar()
        }

    def get_personal_info_dict(self):
        return {
            'user_id': self.id,
            'nickname': self.nickname,
            'avatar': self.get_avatar(),
            'sex': self.sex
        }

    def get_profile_dict(self, page, user_id, identity):
        profile_dict = {
            'user': self.get_self_info_dict(False),
            'followings_count': Fan.query.filter_by(user_id=self.id, is_deleted=False).count(),
            'followers_count': Fan.query.filter_by(idol_id=self.id, is_deleted=False).count(),
            'posts_count': Post.query.filter_by(user_id=self.id, is_deleted=False).count(),
            'posts': self.get_self_posts(page, user_id, identity),
            'is_following': Fan.is_follow(user_id, self.id),
            'is_followed': Fan.is_follow(self.id, user_id)
        }
        return profile_dict

    def get_self_posts(self, page, user_id, identity):
        posts = Post.query.filter_by(user_id=self.id, is_deleted=False).order_by(-Post.created).\
            paginate(page, current_app.config['HOME_PAGE_POSTS_PER_PAGE'], False).items
        return [post.get_post_info_dict(user_id, identity) for post in posts]

    def get_avatar(self):
        return current_app.config['STATIC_URL'] + self.avatar if self.avatar else ''

    def add_golds(self, parameter, method='add', reword=0):
        if parameter == 'post':
            golds = current_app.config['GOLDS_POST']
        elif parameter == 'comment':
            golds = current_app.config['GOLDS_COMMENT']
        elif parameter == 'like':
            golds = current_app.config['GOLDS_LIKE']
        elif parameter == 'reword':
            golds = reword
        else:
            return False
        if method == 'minus' and not reword:
            golds = -golds
        if golds >= 0 or self.golds >= -golds:
            self.golds += golds
            return True
        else:
            return False

    def get_fans(self, following, page, per_page):
        if following:
            return Fan.query.filter_by(user_id=self.id, is_deleted=False).order_by(-Fan.created). \
                paginate(page, per_page, False).items
        else:
            return Fan.query.filter_by(idol_id=self.id, is_deleted=False).order_by(-Fan.created). \
                paginate(page, per_page, False).items

    def get_message_list(self, page):
        message_list = Message.query.filter_by(user_id=self.id).order_by(-Message.created)\
            #  .paginate(page, 20, False).items
        messages = [message.get_detail() for message in message_list]
        return messages

    @staticmethod
    def generate_fake(count=1000):
        from faker import Factory
        fake = Factory.create()
        with open('avatars.txt', 'r') as f:
            avatars = [avatar.replace('\n', '') for avatar in f.readlines()]
        avatar_count = len(avatars)
        for i in range(1, count + 1):
            random_index = randrange(0, avatar_count)
            u = User(
                # id=User.get_random_id(),
                nickname=fake.user_name(),
                email=fake.email(),
                password='123456',
                identity=fake.password(64),
                golds=fake.random_int(),
                signature=fake.sentence(),
                avatar=avatars[random_index]
            )
            db.session.add(u)
        db.session.commit()


class ThirdPartyUser(db.Model):
    __tablename__ = 'third_party_users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    society_user_id = db.Column(db.String(32), nullable=False)
    created = db.Column(db.Integer, default=time_now, nullable=False)
    # 1 QQ, 2 微博
    society_id = db.Column(db.SmallInteger, nullable=False)

    def get_user(self):
        return User.query.get(self.user_id)


class Fan(db.Model):
    __tablename__ = 'fans'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    idol_id = db.Column(db.Integer, nullable=False)
    created = db.Column(db.Integer, default=time_now, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    def get_user_or_idol(self, following):
        if following:
            return User.query.get(self.idol_id)
        else:
            return User.query.get(self.user_id)

    @staticmethod
    def is_follow(user_id, idol_id):
        fan = Fan.query.filter_by(user_id=user_id, idol_id=idol_id, is_deleted=False).limit(1).first()
        return True if fan else False

    @staticmethod
    def generate_fake(count):
        user_count = User.query.count()
        message_type = MessageType.query.filter_by(message_type='follow').first()
        for i in range(1, user_count + 1):
            random_count = randrange(0, count + 1)
            user_set = set()
            for j in range(random_count):
                rand = randrange(1, user_count + 1)
                if rand != i:
                    user_set.add(rand)
            for j in user_set:
                db.session.add(Fan(user_id=i, idol_id=j))
                db.session.add(Message(message_type.id, j, i))
            db.session.commit()


class Collection(db.Model):
    __tablename__ = 'collections'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    created = db.Column(db.Integer, default=time_now, nullable=False)
    image = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Unicode(140), nullable=False)
    channel_id = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)
    likes_count = db.Column(db.Integer, default=0, nullable=False)

    def get_user(self):
        return User.query.get(self.user_id)

    def get_post(self):
        return self

    def report_delete(self):
        reports_count = PostReport.query.filter_by(post_id=self.id).count()
        if self.is_deleted:
            return False
        elif not self.is_deleted and reports_count >= 10:
            self.is_deleted = True
        return self.is_deleted

    def get_post_info_dict(self, user_id='', identity=''):
        post_dict = {
            'user': self.get_user().get_brief_info_dict(),
            'post_id': self.id,
            'content': self.content,
            'created': self.created,
            'channel_id': self.channel_id,
            'image': current_app.config['STATIC_URL'] + self.image,
            'comments_count': PostComment.query.filter_by(post_id=self.id, is_deleted=False).count(),
            'likes_count': self.likes_count,
            'share_count': PostShare.query.filter_by(post_id=self.id).count(),
            'is_liked': PostLike.is_liked(self.id, user_id, identity),
            'is_shared': PostShare.is_shared(self.id, user_id, identity)
        }
        return post_dict

    def get_comments_dict(self, page, per_page, comment_id=None):
        if comment_id:
            comment = PostComment.query.filter_by(post_id=self.id, id=comment_id).limit(1).first()
        else:
            comment = None
        comments = PostComment.query.filter_by(post_id=self.id, is_deleted=False).order_by(-PostComment.created).\
            paginate(page, per_page, False).items
        if comment:
            comment_list = [comment]
            if comment not in comments:
                comment_list.extend(comments)
            else:
                for comment_ in comments:
                    if comment_ not in comment_list:
                        comment_list.append(comment_)
        else:
            comment_list = comments
        return [comment_.get_comment_info() for comment_ in comment_list]

    def add_likes_count(self):
        self.likes_count += 1

    def minus_likes_count(self):
        self.likes_count -= 1

    @staticmethod
    def generate_fake(count):
        from faker import Factory
        zh = Factory.create('zh-CN')
        user_count = User.query.count()
        with open('images.txt', 'r') as f:
            images = [image.replace('\n', '') for image in f.readlines()]
        image_count = len(images)
        fake_func_list = (zh.address, zh.name, zh.company, zh.country) * 4
        for i in range(1, user_count + 1):
            random_count = randrange(0, count + 1)
            for j in range(random_count):
                random_index = randrange(0, image_count)
                content_length = randint(1, 15)
                db.session.add(Post(
                    user_id=i, image=images[random_index], channel_id=randint(1, 4),
                    content=''.join((i() for i in fake_func_list[:content_length])).replace('\n', ''), ))
            db.session.commit()


class PostLike(db.Model):
    __tablename__ = 'post_likes'
    id = db.Column(db.Integer, primary_key=True)
    unified_user_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)

    def __init__(self, post_id, user_id, identity):
        self.post_id = post_id
        self.unified_user_id = UnifiedUser.get_unified_user(user_id, identity).id

    @staticmethod
    def is_liked(post_id, user_id, identity=''):
        if not (user_id or identity):
            return False
        post_like = PostLike.query.filter_by(
            post_id=post_id, unified_user_id=UnifiedUser.get_unified_user(user_id, identity).id
        ).limit(1).first()
        return True if post_like else False

    @staticmethod
    def get_like(post_id, user_id, identity=''):
        return PostLike.query.filter_by(
            post_id=post_id,
            unified_user_id=UnifiedUser.get_unified_user(user_id, identity).id
        ).first()

    def get_post(self):
        return Post.query.get(self.post_id)

    @staticmethod
    def generate_fake(count):
        post_count = Post.query.count()
        user_count = User.query.count()
        for i in range(1, user_count + 1):
            random_count = randrange(0, count + 1)
            post_set = set()
            for j in range(random_count):
                post_set.add(randrange(1, post_count + 1))
            for j in post_set:
                db.session.add(PostLike(user_id=i, post_id=j, identity=''))
            db.session.commit()


class PostReport(db.Model):
    __tablename__ = 'post_reports'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)

    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id

    @staticmethod
    def is_reported(post_id, user_id):
        return PostReport.query.filter_by(post_id=post_id, user_id=user_id).limit(1).first()

    def get_post(self):
        return Post.query.get(self.post_id)


class PostComment(db.Model):
    __tablename__ = 'post_comments'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    x = db.Column(db.Float, nullable=False)
    y = db.Column(db.Float, nullable=False)
    content = db.Column(db.Unicode(24), nullable=False)
    created = db.Column(db.Integer, default=time_now, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False, nullable=False)

    def get_comment_info(self):
        comment_dict = {
            'post_id': self.post_id,
            'created': self.created,
            'content': self.content,
            'x': self.x,
            'y': self.y,
            'user': User.query.get(self.user_id).get_brief_info_dict()
        }
        return comment_dict

    def get_post(self):
        return Post.query.get(self.post_id)

    def report_delete(self):
        reports_count = PostCommentReport.query.filter_by(post_comment_id=self.id).count()
        if self.is_deleted:
            return False
        elif not self.is_deleted and reports_count >= 10:
            self.is_deleted = True
        return self.is_deleted

    @staticmethod
    def generate_fake(count):
        from faker import Factory
        zh = Factory.create('zh-CN')
        post_count = Post.query.count()
        user_count = User.query.count()
        fake_func_list = (zh.address, zh.name, zh.company, zh.country)
        message_type = MessageType.query.filter_by(message_type='comment').first()
        for i in range(1, user_count + 1):
            random_count = randrange(0, count + 1)
            post_set = set()
            for j in range(random_count):
                post_set.add(randrange(1, post_count + 1))
            for j in post_set:
                content_length = randint(1, 4)
                comment = PostComment(
                    user_id=i, post_id=j, x=random(), y=random(),
                    content=''.join((i() for i in fake_func_list[:content_length])).replace('\n', ''))
                db.session.add(comment)
                db.session.add(Message(message_type.id, Post.query.get(j).get_user().id, i, comment.id))
            db.session.commit()


class PostShare(db.Model):
    __tablename__ = 'post_shares'
    id = db.Column(db.Integer, primary_key=True)
    unified_user_id = db.Column(db.Integer, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    society_id = db.Column(db.SmallInteger, nullable=False)

    def __init__(self, post_id, society_id, user_id, identity):
        self.post_id = post_id
        self.society_id = society_id
        self.unified_user_id = UnifiedUser.get_unified_user(user_id, identity).id

    @staticmethod
    def is_shared(post_id, user_id, identity=''):
        if not (user_id or identity):
            return False
        post_share = PostShare.query.filter_by(
            post_id=post_id, unified_user_id=UnifiedUser.get_unified_user(user_id, identity).id
        ).limit(1).first()
        return True if post_share else False

    @staticmethod
    def generate_fake(count):
        post_count = Post.query.count()
        user_count = User.query.count()
        for i in range(1, user_count + 1):
            random_count = randrange(0, count + 1)
            post_set = set()
            for j in range(random_count):
                post_set.add(randrange(1, post_count + 1))
            for j in post_set:
                db.session.add(PostShare(post_id=j, society_id=randrange(1, 5), user_id=i, identity=''))
            db.session.commit()


class PostCommentLike(db.Model):
    __tablename__ = 'post_comment_likes'
    id = db.Column(db.Integer, primary_key=True)
    unified_user_id = db.Column(db.Integer, nullable=False)
    post_comment_id = db.Column(db.Integer, nullable=False)

    def __init__(self, post_comment_id, user_id, identity):
        self.post_comment_id = post_comment_id
        self.unified_user_id = UnifiedUser.get_unified_user(user_id, identity).id

    @staticmethod
    def is_liked(post_comment_id, user_id, identity=''):
        if not (user_id or identity):
            return False
        post_comment_like = PostCommentLike.query.filter_by(
            post_comment_id=post_comment_id, unified_user_id=UnifiedUser.get_unified_user(user_id, identity).id
        ).limit(1).first()
        return True if post_comment_like else False

    @staticmethod
    def get_like(post_id, user_id, identity=''):
        return PostCommentLike.query.filter_by(
            post_id=post_id,
            unified_user_id=UnifiedUser.get_unified_user(user_id, identity).id
        ).first()

    def get_post(self):
        return Post.query.get(self.post_id)


class PostCommentReport(db.Model):
    __tablename__ = 'post_comment_reports'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    post_comment_id = db.Column(db.Integer, nullable=False)

    def __init__(self, post_comment_id, user_id):
        self.post_comment_id = post_comment_id
        self.user_id = user_id

    @staticmethod
    def is_reported(post_comment_id, user_id):
        return PostCommentReport.query.filter_by(post_comment_id=post_comment_id, user_id=user_id).limit(1).first()

    def get_post(self):
        return Post.query.get(self.post_id)


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.Integer, default=time_now, nullable=False)
    message_type_id = db.Column(db.SmallInteger, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    launch_id = db.Column(db.Integer, nullable=False)
    post_comment_id = db.Column(db.Integer, nullable=False)

    def __init__(self, message_type_id, user_id, launch_id, post_comment_id=0):
        self.message_type_id = message_type_id
        self.user_id = user_id
        self.launch_id = launch_id
        self.post_comment_id = post_comment_id

    def get_detail(self):
        message_type = MessageType.query.get(self.message_type_id)
        detail = {
            'message_type': message_type.type,
            'created': self.created
        }
        if message_type.type == 'comment' or message_type.type == 'follow':
            launch = User.query.get(self.launch_id)
            detail['user'] = launch.get_brief_info_dict()
            if message_type.type == 'comment':
                detail['post_comment_id'] = self.post_comment_id
                post_comment = PostComment.query.get(self.post_comment_id)
                detail['post_id'] = post_comment.post_id
                detail['content'] = post_comment.content
                detail['format'] = u'biu了你的图片'
            else:
                detail['format'] = u'关注了你'
        else:
            detail['format'] = u'你的图片包含政治不正确的信息哦，我已经报警了!'
        return detail

    @staticmethod
    def generate():
        message_type = MessageType.query.filter_by(type='comment').first()
        comments = PostComment.query.all()
        for comment in comments:
            launch = User.query.get(comment.user_id)
            user = User.query.get(comment.get_post().get_user().id)
            db.session.add(Message(message_type.id, user.id, launch.id, comment.id))
        db.session.commit()
        message_type = MessageType.query.filter_by(type='follow').first()
        fans = Fan.query.all()
        for fan in fans:
            launch = fan.get_user_or_idol(0)
            user = fan.get_user_or_idol(1)
            db.session.add(Message(message_type.id, user.id, launch.id))
        db.session.commit()


class MessageType(db.Model):
    __tablename__ = 'message_types'
    id = db.Column(db.SmallInteger, primary_key=True)
    type = db.Column(db.String(20), nullable=False)

    @staticmethod
    def generate():
        db.session.add(MessageType(type='comment'))
        db.session.add(MessageType(type='follow'))
        db.session.add(MessageType(type='delete_post'))
        db.session.commit()


class Channel(db.Model):
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)
    channel = db.Column(db.Unicode(30), nullable=False)
    panel = db.Column(db.String(64), nullable=False)
    navbar = db.Column(db.String(64), nullable=False)

    def get_channel(self):
        return {
            'channel_id': self.id,
            'channel': self.channel,
            'panel': current_app.config['STATIC_URL'] + self.panel,
            'navbar': current_app.config['STATIC_URL'] + self.navbar
        }

    @staticmethod
    def generate():
        db.session.add(Channel(channel=u'你开心就好', panel=u'channels/Channel1.png', navbar=u'channels/NavBar1.png'))
        db.session.add(Channel(channel=u'涨姿势', panel=u'channels/Channel2.png', navbar=u'channels/NavBar2.png'))
        db.session.add(Channel(channel=u'脑洞是第一生产力', panel=u'channels/Channel3.png', navbar=u'channels/NavBar3.png'))
        db.session.add(Channel(channel=u'那么问题来了', panel=u'channels/Channel4.png', navbar=u'channels/NavBar4.png'))
        db.session.add(Channel(channel=u'全明星阵容', panel=u'channels/Channel5.png', navbar=u'channels/NavBar5.png'))
        db.session.commit()


class Society(db.Model):
    __tablename__ = 'societies'
    id = db.Column(db.SmallInteger, primary_key=True)
    society = db.Column(db.Unicode(8), nullable=False)

    @staticmethod
    def generate():
        db.session.add(Society(society=u'QQ'))
        db.session.add(Society(society=u'微博'))
        db.session.add(Society(society=u'微信'))
        db.session.add(Society(society=u'QQ空间'))
        db.session.commit()


def generate_helper_data():
    Channel.generate()
    Society.generate()
    MessageType.generate()


def generate_fake_data(user_count=1000, fan_count=100, post_count=15, post_like_count=100,
                       post_share_count=100, post_comment_count=100):
    User.generate_fake(user_count)
    Fan.generate_fake(fan_count)
    Post.generate_fake(post_count)
    PostLike.generate_fake(post_like_count)
    PostShare.generate_fake(post_share_count)
    PostComment.generate_fake(post_comment_count)
    for post in Post.query.all():
        post.likes_count = PostLike.query.filter_by(post_id=post.id).count()


def generate_fake_image_path():
    with open('images.txt', 'r') as f:
        images = [line.replace('\n', '') for line in f.readlines()]
    posts = Post.query.all()
    for post in posts:
        post.image = images[randrange(0, len(images))]


def test_message():
    from utils import push
    push('comment', User.query.get(4), User.query.get(1), u'富贵全靠大左')