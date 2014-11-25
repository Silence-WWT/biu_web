Biu API Doc
===

register
---
    URL:
        /api/v1.0/register?username=&password=&identity=&mobile=
    method:
        get
    parameters:
        username
        password
        identity: uuid
        mobile: 后端先不检测，因为目前还没确定注册是否需要手机号……
    json:
        {"status": 0, "message": "success", "user": {"user_id": "", "username": "", "mobile": "", "identity": "",
            "golds": "", "avatar": "", "signature": "", "push": "", "disturb": ""}}
            
        status: 0 for success, 1001 for username exists, 2000 for parameter error
        message: message of status code
        user: a dict of user's info
            user_id
            username
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
        /api/v1.0/login?username=&password=&identity=
    method:
        get
    parameters:
        username
        password
        identity
    json:
        {"status": 0, "message": ""}
        
        status: 0 for success, 1000 for login fail
        message: message of status
        
push_setting
---
    URL:
        /api/v1.0/push_setting?user_id=&push=&disturb=
    method:
        get
    parameters:
        user_id
        push
        disturb: push, disturb 可只传其中一个, 且必须为int
    json:
        {"status": 0, "message": ""}
        
        status: 0 for success, 1002 for user not exists
        message: message of status
        
post_comment
---
    URL:
        /api/v1.0/post_comment?user_id=&post_id=&content=&post_id=&x=&y=
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
            "user": {"user_id": "", "username": "", "avatar": ""}}}
        
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
                username
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
        