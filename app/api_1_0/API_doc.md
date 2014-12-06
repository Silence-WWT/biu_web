Biu API Doc
===


third_party_token
---
    第三方登录前必须先调用这个接口获取token, 第三方登录时, 再将根据MD5加密过的token返回
    URL:
        /api/v1.0/third_party_token?identity=
    method:
        get
    parameters:
        identity: uuid
    json:
        {"status": 0, "message": "success", "token": ""}
        
        status: int, 0 for success, 2001 for message confirm fail
        message: str, message of status code
        token: str


confirm_mobile
---
    URL:
        /api/v1.0/confirm_mobile
    method:
        get
    json:
        {"status": 0, "message": "success"}
        
        status: int, 0 for success, 2001 for message confirm fail
        message: str, message of status code
        

register
---
    URL:
        /api/v1.0/register?password=&identity=&mobile=&captcha=
    method:
        get
    parameters:
        password
        identity: uuid
        mobile: 必须
        captcha
    json:
        {"status": 0, "message": "success", "user": {"user_id": "", "nickname": "", "mobile": "",
            "identity": "", "golds": "", "avatar": "", "signature": "", "push": "", "disturb": ""}}
            
        status: int, 0 for success, 1001 for mobile exists, 2000 for parameter error, 1005 for captcha incorrect
        message: str, message of status code
        user: a dict of user's info
            user_id: int
            nickname: unicode
            mobile: str
            identity: str
            golds: 金币 int
            avatar: 头像 str
            signature: 个人签名 unicode
            push: 是否推送消息 bool
            disturb: 夜间是否推送消息 bool
            

login
---
    URL:
        /api/v1.0/login?mobile=&password=&identity=
    method:
        get
    parameters:
        mobile
        password
        identity
    json:
        {"status": 0, "message": "success", "user": {"user_id": "", "nickname": "", "mobile": "", "identity": "",
            "golds": "", "avatar": "", "signature": "", "push": "", "disturb": "", "sex": ""}}
            
        status: int, 0 for success, 1000 for login fail, 2000 for parameter error
        message: str, message of status code
        user: a dict of user's info
            user_id: int
            mobile: str
            nickname: unicode
            mobile: str
            identity: str
            golds: 金币 int
            avatar: 头像 int
            signature: 个人签名 unicode
            push: 是否推送消息 bool
            disturb: 夜间是否推送消息 bool
            sex: 0 for female, 1 for male, 2 for unknown


follow
---
    URL:
        /api/v1.0/follow?user_id=&idol_id=&cancel=
    method:
        get
    parameters:
        user_id
        idol_id: 需要关注的偶像的id
        cancel: 取消关注，默认为0
    json:
        {"status": 0, "message": "success"}
        
        status: int, 0 for success, 2000 for parameters error
        message: str, message of status code


follow_list
---
    URL:
        /api/v1.0/follow_list?user_id=&target_id=&following=&page=
    method:
        get
    parameters:
        user_id: 用户id, 如果用户未登录可不传或传空
        target_id: 所要查看关注列表的用户的id， 如果查看自己的关注列表，可不传
        following: default 1, 1 for 粉丝列表， 0 for 被关注的列表
        page: default 1
    json:
        {"status": 0, "message": "success", "follows": [{"user_id": "", "nickname": "", "avatar": "",
            "is_followed": "", "is_following": ""]}
        
        status: int, 0 for success, 2000 for parameters error
        message: str, message of status code
        follows: a list of users
            user_id: int
            nickname: unicode
            avatar: str
            is_followed: 调用这个接口的用户是否已被该用户关注 bool
            is_following: 调用这个接口的用户是否已关注该用户 bool


personal_info_setting
---
    URL:
        /api/v1.0/personal_info_setting?user_id=&image_str=&nickname=&signature=&sex=
    method:
        get
    parameters:
        user_id
        image_str: base64 string 如果用户没有更换头像，可以为空
        nickname: 无论用户是否重新设置了昵称和签名，每次调用接口都必须发送当前的昵称、签名和性别
        signature
        sex: 0 for female, 1 for male, 2 for unknown
    json:
        {"status": 0, "message": "success"}
        
        status: int, 0 for success, 1004 for invalid image, 1002 for user not exists
        message: str, message of status code
        
        
push_setting
---
    URL:
        /api/v1.0/push_setting?user_id=&push=&disturb=
    method:
        get
    parameters:
        user_id
        push
        disturb: push, disturb 可只传其中一个, 且必须为0 或 1
    json:
        {"status": 0, "message": ""}
        
        status: int, 0 for success, 1002 for user not exists
        message: str, message of status
        
        
profile
---
    URL:
        /api/v1.0/profile?user_id=&page=
    method:
        get
    parameters:
        user_id
        page: default 1, page of user's posts
    json:
        {"status": 0, "message": "success", "profile": {"followings_count": "", "followers_count": "", "is_followed": "",
             "is_following": "", "posts_count": "", "likes_count": "", "share_count": "",
             "user": {"user_id": "", "nickname": "", "golds": "", "avatar": "", "signature": ""},
             "posts": [{"channel_id": "", "content": "", "created": "", "image": "", "post_id": "", "comments_count": "", 
                "is_liked": "", "user": {"avatar": "", "user_id": "", "nickname": ""}}]}}
        
        status: int, 0 for success, 1002 for user not exist
        message: str, message of status code
        profile: a dict of user's profile
            followings_count: int
            followers_count: int
            posts_count: int
            is_followed: 调用这个接口的用户是否已被该用户关注 bool
            is_following: 调用这个接口的用户是否已关注该用户 bool
            user: a dict of user info
                user_id: int
                nickname: unicode
                golds: int
                avatar: str
                signature
            posts: a list of post dict
                post_id: int
                channel_id: int
                content: unicode
                created: int
                image: str
                comments_count
                likes_count: int
                share_count: int
                is_liked: bool
                user: a dict of user info
                    user_id: int
                    nickname: unicode
                    avatar: str


post
---
    URL:
        /api/v1.0/post      目前暂时在浏览器里用get方式直接打开可以上传图片
    method:
        get
    parameters:
        user_id
        content
        channel_id
        image_str: base64 string
    json:
        {"status": 0, "message": "success", "post": {"channel_id": "", "content": "", "created": "", "image": "",
            "comments_count": "", "post_id": "", "likes_count": "", "share_count": "",
            "user": {"avatar": "", "user_id": "", "nickname": ""}}}
        
        status: int, 0 for success, 2000 for parameter error
        message: str, message of status code
        post: a dict of post
            post_id: int
            created: int
            image: str
            content: unicode
            channel_id: int
            comments_count
            likes_count: int
            share_count: int
            user: a dict of user
                user_id: int
                avatar: str
                nickname: unicode
        
        
post_comment
---
    URL:
        /api/v1.0/post_comment?user_id=&post_id=&content=&x=&y=
    method:
        get
    parameters:
        user_id
        post_id
        content
        x
        y
    json:
        {"status": 0, "message": "", "post_comment": {"post_id": "", "created": "", "content": "", "x": "", "y": "",
            "user": {"user_id": "", "nickname": "", "avatar": ""}}}
        
        status: int, 0 for success, 1002 for user not exists, 2000 for parameter error
        message: str, message of status
        post_comment: a dict of comment
            post_id: int
            created: 弹幕发送的时间，1970.1.1 开始的秒数
            content: unicode
            x: float
            y: float
            user: a dict of user
                user_id: int
                nickname: unicode
                avatar: str
                
                
get_channels
---
    URL:
        /api/v1.0/get_channels
    method:
        get
    json:
        {"status": 0, "message": "success", "channels": [{"channel_id": "", "channel": ""}]}
        
        status: int, 0 for success
        message: str, message of status code
        channels: a list of all channels dict
            channel_id: int
            channel: unicode name of channel
            
            
get_posts
---
    URL:
        /api/v1.0/get_posts?user_id=&channel_id=&page=
    method:
        get
    parameters:
        user_id: 仅当请求关注用户的图片列表时需要使用该参数
        channel_id: default -3. -3: 热门, -2: 最新发布, -1: 关注用户发布, >0: 正常的其他频道.
                    为了保证将来的扩展性，我觉得第一版 channel的id与名称还是全部由服务器返回，频道的图标最好也由服务器返回（当然这个我还没实现）
                    热门，最新发布，关注用户 不能算真正意义上的"频道"， 而且其他的频道id都是与数据库中的id刚好对应的
        page: default 1
    json:
        {"status": 0, "message": "success",
         "posts": [{"channel_id": "", "content": "", "created": "", "image": "", "comments_count": "", "post_id": "",
            "likes_count": "", "share_count": "", "is_liked": "",
            "user": {"avatar": "", "user_id": "", "nickname": ""},
            "comments": [{"post_id": "", "created": "", "content": "", "x": "", "y": "",
                "user": {"user_id": "", "nickname": "", "avatar": ""}}]]}
        
        status: int, 0 for success, 1002 for user not exist
        message: str, message for status code
        posts: a list of post dict
            post_id: int
            created: int
            image: str
            content: unicode
            channel_id: int
            comments_count: int
            likes_count: int
            share_count: int
            is_liked: bool
            user: a dict of user
                user_id: int
                avatar: str
                nickname: unicode
            comments: a list of comments dict in first page
                post_id: int
                created: 弹幕发送的时间，1970.1.1 开始的秒数  int
                content: unicode
                x: float
                y: float
                user: a dict of user
                    user_id: int
                    nickname: unicode
                    avatar:: str


get_post_comments
---
    URL:
        /api/v1.0/get_post_comments?post_id=&page=
    method:
        get
    parameters:
        post_id
        page: default 1
    json:
        {"status": 0, "message": "success", "comments": [{"post_id": "", "created": "", "content": "", "x": "", "y": "",
            "user": {"user_id": "", "nickname": "", "avatar": ""}}]}
            
        status: int, 0 for success, 2000 for post not exist
        message: str, message of status code
        comments: a list of comments
            post_id: int
            created: int
            content: unicode
            x: float
            y: float
            user: a dict of user
                user_id: int
                nickname: unicode
                avatar: str


like
---
    URL:
        /api/v1.0/like?user_id=&target_id=&cancel=&type=
    method:
        get
    parameters:
        user_id
        target_id: 图片或弹幕的id, 因为点赞的机制基本相同，所以就使用同一个接口了……
        cancel: 是否取消, 默认为0
        type: "post" OR "post_comment"
    json:
        {"status": 0, "message": ""}
        
        status: int, 0 for success, 2000 for parameter error
        message: str, message of status
        
        
report
---
    URL:
        /api/v1.0/report?user_id=&target_id=&type=
    method:
        get
    parameters:
        user_id
        target_id: 图片或弹幕的id, 因为举报的机制基本相同，所以就使用同一个接口了……
        type: "post" OR "post_comment"
    json:
        {"status": 0, "message": ""}
        
        status: int, 0 for success, 2000 for parameter error
        message: str, message of status


up_reword
---
    URL:
        /api/v1.0/up_reword?user_id=&up_id=&golds=
    method:
        get
    parameters:
        user_id
        up_id: up主的id,无法打赏自己
        golds: 打赏的金币,必须大于0
    json:
        {"status": 0, "message": "success"}
        
        status: int, 0 for success, 1003 for user's golds not enough, 2000 for parameter error
        message: str, message for status code
        