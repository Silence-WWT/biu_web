/*------------------------- 获取信息 -------------------------*/
function get_info() {
	pic_id = localStorage.getItem('post');
	$.ajax({
		url : 'http://123.56.45.108:82/api/v1.0/post/share?post=' + pic_id,
		type: 'GET',
		dataType:'json',
		timeout: 5000,
		success : function(data) {
			if(data.status == 0){
				closeLoading();
				var MainW = $(document.body).width();
				$('#pic').css('margin-left','');
				$('#pic').css('margin-top','');
				$('#pic').css('height','auto');
				$('#pic').css('width','100%');
				$('#pic').css('opacity','1');
				$('#pic').attr('src',data.post.image);
				$('#main_user_headphoto').attr('src',data.post.user.avatar);
				$('#main_user_name').text(data.post.user.nickname);
				var tmpdate = parseInt(data.post.created*1000);
				var date = encodeDate(tmpdate);
				$('#main_user_time').text(date);
				$('#biu_count').text(data.post.comments_count);
				$('#main_user_content').text(data.post.content);
				var contents_data = data.post.comments;
				for (var i = 0;i < contents_data.length;i++) {
					var tmp_data = contents_data[i];
					var tmp_length = tmp_data.content.length;
					if ((tmp_length*12+10) < (MainW-MainW*(tmp_data.x))) {
						var html = "<div id='my_" + i + "' style='height:30px;background-color: rgba(0,0,0,0.4);border-radius: 3px;padding-left: 5px;padding-right: 5px;position: absolute;top:" + MainW*(tmp_data.y) + "px;left:" + MainW*(tmp_data.x) + "px;text-align: left;'><img src='" + tmp_data.user.avatar + "' style='border-radius: 3px;height: 24px;width: 24px;margin-top: 3px;' /><font class='font_face' style='margin-left: 5px;font-size: 12px;line-height: 20px;color: white;'>" + tmp_data.content + "</font></div>";
					} else {
						var html = "<div id='my_" + i + "' style='height:30px;background-color: rgba(0,0,0,0.4);border-radius: 3px;padding-left: 5px;padding-right: 5px;position: absolute;top:" + MainW*(tmp_data.y) + "px;right: " + (MainW/2 - MainW/2*(tmp_data.x)) + "px;text-align: right;'><font class='font_face' style='margin-right: 5px;font-size: 12px;line-height: 20px;color: white;'>" + tmp_data.content + "</font><img src='" + tmp_data.user.avatar + "' style='border-radius: 3px;height: 24px;width: 24px;margin-top: 3px;' /></div>";
					}
					$('#content_div').append(html);
				}

				WeixinApi.ready(function(Api) {
					// 微信分享的数据
					var wxData = {
						"appId": '微信App key',
						"imgUrl": data.post.user.avatar,// 分享出去的小头像
						"link": '线上的网址传参数方式  ?id=' + pic_id,
						"desc": data.post.user.nickname,//分享给微信好友的描述
						"title": data.post.user.nickname,//分享到朋友圈和好友的标题
					};
					// 分享的回调
					var wxCallbacks = {};
					// 用户点开右上角popup菜单后，点击分享给好友，会执行下面这个代码
					Api.shareToFriend(wxData, wxCallbacks);
					// 点击分享到朋友圈，会执行下面这个代码
					Api.shareToTimeline(wxData, wxCallbacks);
					// 点击分享到腾讯微博，会执行下面这个代码
					Api.shareToWeibo(wxData, wxCallbacks);
					// iOS上，可以直接调用这个API进行分享，一句话搞定
					Api.generalShare(wxData,wxCallbacks);
				});
			} else {
			}
		},
		error: function(){
		}
	});
}

/*------------------------- 时间转换 -------------------------*/
function encodeDate(time){
     var date = new Date(time);
     var year = date.getFullYear();
     var month = date.getMonth()+1;
     var day = date.getDate();
     var hour = date.getHours();
     var minutes = date.getMinutes();
     var second = date.getSeconds();
	 var result = year + "年" + month + "月" + day + "日  " + hour + "时" + minutes + "分" + second + "秒";
	 return result;
}

/*------------------------- open loading -------------------------*/
function showLoading() {
	var tmp = document.getElementById('loading_bg');
	if (tmp == null) {
		var html = "<div id='loading_bg'><img class='loading_icon' src='http://biu2014.qiniudn.com/static/img/icon_loading.png'></img></div>";
		$(document.body).append(html);
	}
}

/*------------------------- close loading -------------------------*/
function closeLoading() {
	var tmp = document.getElementById('loading_bg');
	if (tmp != null) {
		$('#loading_bg').remove();
	}
}
