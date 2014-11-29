Biu API Doc
===

register
---
    URL:
        /api/v1.0/register?password=&identity=&mobile=
    method:
        get
    parameters:
        password
        identity: uuid
        mobile: 后端先不检测，因为目前还没确定注册是否需要手机号……
    json:
        {"status": 0, "message": "success", "user": {"user_id": "", "nickname": "", "mobile": "",
            "identity": "", "golds": "", "avatar": "", "signature": "", "push": "", "disturb": ""}}
            
        status: 0 for success, 1001 for mobile exists, 2000 for parameter error
        message: message of status code
        user: a dict of user's info
            user_id
            nickname
            mobile
            identity
            golds: 金币
            avatar: 头像
            signature: 个人签名
            push: 是否推送消息
            disturb: 夜间是否推送消息
            
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
            "golds": "", "avatar": "", "signature": "", "push": "", "disturb": ""}}
            
        status: 0 for success, 1000 for login fail, 2000 for parameter error
        message: message of status code
        user: a dict of user's info
            user_id
            mobile
            nickname
            mobile
            identity
            golds: 金币
            avatar: 头像
            signature: 个人签名
            push: 是否推送消息
            disturb: 夜间是否推送消息

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
        
        status: 0 for success, 2000 for parameters error
        message: message of status code

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
        {"status": 0, "message": "success", "follows": [{"user_id": "", "nickname": "", "avatar": "", "followed": ""]}
        
        status: 0 for success, 2000 for parameters error
        message: message of status code
        follows: a list of users
            user_id
            nickname
            avatar
            followed: 调用这个接口的用户是否已关注该用户

personal_info_setting
---
    URL:
        /api/v1.0/personal_info_setting    目前暂时在浏览器里用get方式直接打开可以上传图片
    method:
        post
    parameters:
        user_id
        image: 如果用户没有更换头像，可以为空
        nickname: 无论用户是否重新设置了昵称和签名，每次调用接口都必须发送当前的昵称和签名
        signature
    json:
        {"status": 0, "message": "success"}
        
        status: 0 for success, 1004 for valid image, 1002 for user not exists
        message: message of status code
        
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
        
        status: 0 for success, 1002 for user not exists
        message: message of status
        
post
---
    URL:
        /api/v1.0/post      目前暂时在浏览器里用get方式直接打开可以上传图片
    method:
        post
    parameters:
        user_id
        content
        channel_id
        image
    json:
        {"status": 0, "message": "success", "post": {"channel_id": "", "content": "", "created": "", "image": "",
            "post_id": "", "user": {"avatar": "", "user_id": "", "nickname": ""}}}
        
        status: 0 for success, 2000 for parameter error
        message: message of status code
        post: a dict of post
            post_id
            created
            image
            content
            channel_id
            user: a dict of user
                user_id
                avatar
                nickname
        
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
        
        status: 0 for success, 1002 for user not exists, 2000 for parameter error
        message: message of status
        post_comment: a dict of comment
            post_id
            created: 弹幕发送的时间，1970.1.1 开始的秒数
            content
            x
            y
            user: a dict of user
                user_id
                nickname
                avatar
                
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
            
        status: 0 for success, 2000 for post not exist
        message: message of status code
        comments: a list of comments
            post_id
            created
            content
            x
            y
            user: a dict of user
                user_id
                nickname
                avatar

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
        
        status: 0 for success, 2000 for parameter error
        message: message of status
        
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
        
        status: 0 for success, 2000 for parameter error
        message: message of status

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
        
        status: 0 for success, 1003 for user's golds not enough, 2000 for parameter error
        message: message for status code
        