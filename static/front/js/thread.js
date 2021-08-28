$(function () {
    $.event.addProp('dataTransfer');
    var ue = UE.getEditor("editor", {
        'serverUrl': '/ueditor/upload/',
        toolbars: [[
            'undo', //撤销
            'redo', //重做
            'bold', //加粗
            'italic', //斜体
            'source', //源代码
            'blockquote', //引用
            'selectall', //全选
            'insertcode', //代码语言
            'fontfamily', //字体
            'fontsize', //字号
            'simpleupload', //单图上传
            'emotion' //表情
        ]]
    });
    window.ue = ue;


    $('#publish-comment-btn').click(function () {
        var is_loginE = $('#login_flag');
        var is_login = is_loginE.attr('is_login');
        if (!is_login) {
            window.location = '/login/'
        }
        var author_id = is_loginE.attr('author_id');
        var content = window.ue.getContent();
        var thread_id = is_loginE.attr('thread_id');

        zlajax.post({
            'url': '/add_comment/',
            'data': {
                'content': content,
                'author_id': author_id,
                'thread_id': thread_id
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    xtalert.alertSuccessToast('评论成功');
                    setTimeout(function () {
                        window.location.reload()
                    }, 600)
                } else {
                    xtalert.alertInfo(data['message'])
                }
            },
            'fail': function () {
                xtalert.alertNetworkError()
            }
        })

    });

    function safeStr(str){
        return str.replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g, "&quot;").replace(/'/g, "&#039;");
    }

    $('.publish-child-comment-btn').click(function (e) {
        e.preventDefault();
        var curBtn = $(this);
        var cid = curBtn.attr('cid');
        console.log('cid', cid);
        var childComments = $('div[pcid="' + cid + '"]');
        var content = safeStr(curBtn.parent().prev().children(0).val());
        var is_loginE = $('#login_flag');
        var is_login = is_loginE.attr('is_login');
        if (!is_login) {
            window.location = '/login/'
        }
        var author_id = is_loginE.attr('author_id');
        var thread_id = is_loginE.attr('thread_id');
        var parent_id = curBtn.attr('cid');


        zlajax.post({
            'url': '/add_child_comment/',
            'data': {
                'content': content,
                'author_id': author_id,
                'thread_id': thread_id,
                'parent_id': parent_id
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    var data = data['data'];
                    var insertHTML = `
                                    <div class="child-comment col-sm-8" pcid="${cid}">
                                        <p class="username">${data['username']}评论于刚刚
                                            <span class="pull-right">0</span>
                                            <span class="glyphicon glyphicon-thumbs-up com-like-btn pull-right"
                                                  cid="${data['id']}"></span>


                                            <a href="#" class="com-del-btn" cid="${data['id']}">删除</a>

                                        <p>${data['content']}</p>
                                        </p>
                                    </div>
                    `;
                    // var childComments = $('.child-comment').attr('pcid', cid);
                    // var childCommentsCount = childComments.length;
                    // var lastchildComment = childComments.last();
                    console.log('len', childComments.length);
                    if (childComments.length < 5) {
                        console.log(childComments.eq(0).parent());
                        childComments.eq(0).parent().prepend(insertHTML);
                    } else {
                        childComments.eq(0).parent().prepend(insertHTML);
                        console.log('lasts', childComments.last());
                        childComments.last().remove();

                    }
                    // console.log(childCommentsCount);
                    // console.log(lastchildComment);
                    // // if
                    // firstChildComment.prepend(insertHTML);
                } else {
                    xtalert.alertInfo(data['message'])
                }
            },
            'fail': function () {
                xtalert.alertNetworkError()
            }
        })

    });

    $('.option').click(function (e) {
        $(this).css('background-color', 'rgba(185, 185, 185, 0.45)');
        var front_user = $('#login_flag').attr('is_login');
        if (front_user != '1') {
            window.location.href = '/login/';
            return
        }
        var type = $(this).attr('flag');
        var url = '';
        if (type == '1') {
            url = '/like/'
        } else {
            url = url = '/collect/'
        }
        var thread_id = $('.header').attr('thread_id');
        zlajax.get({
            'url': url + thread_id,
            'success': function (data) {
                if (data['code'] == 200) {
                    xtalert.alertSuccessToast('操作成功');
                } else {
                    xtalert.alertInfo(data['message'])
                }
            },
            'fail': function () {
                xtalert.alertNetworkError()
            }
        })
    });

    $('#delete-thread').click(function (e) {
        var thread_id = $('.header').attr('thread_id');
        xtalert.alertConfirm({
            title: '确定删除吗',
            confirmCallback: function () {
                zlajax.get({
                    'url': '/delitem/?iid=' + thread_id,
                    'success': function (data) {
                        if (data['code'] == 200) {
                            window.location.href = '/'
                        } else {
                            xtalert.alertInfo(data['message'])
                        }
                    },
                    'fail': function () {
                        xtalert.alertNetworkError()
                    }
                })
            }
        })
    });

    $('#edit-thread').click(function (e) {
        e.preventDefault();
        tid = $(this).attr('tid');
        window.location.href = '/thread?tid=' + tid
    });


    $('.com-del-btn').click(function (e) {
        e.preventDefault();
        var curEle = $(this);
        var cid = curEle.attr('cid');
        var curComItem = curEle.parent().parent();
        var parentComment = curEle.attr('parent-comment');
        zlajax.delete({
            'url': '/del_comment/' + cid,
            'success': function (data) {
                if (data['code'] == 200) {
                    if (parentComment) {
                        curComItem.parent().remove();
                    } else {
                        curComItem.remove();
                    }
                } else {
                    xtalert.alertInfo(data['message'])
                }
            },
            'fail': function () {
                xtalert.alertNetworkError()
            }
        })

    });

    $('.com-like-btn').click(function (e) {
        e.preventDefault();
        var curEle = $(this);
        if ( $('#login_flag').length === 0 ) {
            xtalert.alertInfoToast('请先登录');
            return;
        }

        var nextEle = curEle.next();
        var curLikeNum = parseInt(nextEle.text());
        var cid = curEle.attr('cid');
        zlajax.post({
            'url': '/threads/comment-like/' + cid,
            'success': function (data) {
                if (data['code'] == 200) {
                    nextEle.text(curLikeNum + 1);
                    curEle.css({'background-color': 'rgba(255, 166, 40, 0.49)', 'border-radius': '20%'});
                } else {
                    xtalert.alertInfo(data['message'])
                }
            },
            'fail': function () {
                xtalert.alertNetworkError()
            }
        })
    });

    $('.loadMoreCom').click(function () {
        var curEle = $(this);
        var cid = curEle.attr('cid');
        var uid = curEle.attr('uid');
        $('.remove-more-comm-btn[cid="' + cid + '"]').text('收起评论').addClass('glyphicon').addClass('glyphicon-chevron-up');
        console.log('cid', cid);
        console.log('uid', uid);
        var curPage = curEle.attr('cur-page');
        console.log(curPage);

        zlajax.get({
            'url': '/threads/comment/' + cid + '?page=' + (parseInt(curPage) + 1),
            'data': '',
            'success': function (data) {

                var childCommentArea = $('div[pcid="' + cid + '"]').eq(0).parent();
                var dataList = data['data'];
                if (dataList.length === 0) {
                    $('.loadMoreCom[cid="' + cid + '"]').text('到底啦(≧▽≦)~');
                }


                dataList.forEach(item => childCommentArea.append(
                    item['uid'] == uid ?
                        `
                            <div class="child-comment col-sm-8" pcid="${cid}">
                                <p class="username">${item['username']}评论于${item['create_time']}
                                    <span class="pull-right">0</span>
                                    <span class="glyphicon glyphicon-thumbs-up com-like-btn pull-right"
                                          cid="${item['id']}"></span>
                                    <a href="#" class="com-del-btn" cid="${item['id']}">删除</a>
                                    <p>${item['content']}</p>
                                </p>
                             </div>
                        `
                        :
                        `
                            <div class="child-comment col-sm-8" pcid="${cid}">
                                <p class="username">${item['username']}评论于${item['create_time']}
                                    <span class="pull-right">0</span>
                                    <span class="glyphicon glyphicon-thumbs-up com-like-btn pull-right"
                                          cid="${item['id']}"></span>
                                    <p>${item['content']}</p>
                                </p>
                             </div>
                          `
                ));
                curEle.attr('cur-page', parseInt(curPage) + 1);
            }
        })
    });

    $('.remove-more-comm-btn').click(function () {
        var curEle = $(this);
        var cid = curEle.attr('cid');
        var childComments = $('div[pcid="' + cid + '"]');
        var childCommentArea = childComments.eq(0).parent();
        var firstFiveComments = childComments.slice(0, 5);
        childCommentArea.empty();
        childCommentArea.append(firstFiveComments);
        curEle.text('');
        curEle.removeClass('glyphicon');
        curEle.removeClass('glyphicon-chevron-up');
        $('.loadMoreCom[cid="' + cid + '"]').text('加载更多').attr('cur-page', 1);
    });

    $('.copyCurrentUrl').click(function () {
        var dummy = document.createElement('input');
        var text = window.location.href;
        document.body.appendChild(dummy);
        dummy.value = text;
        dummy.select();
        document.execCommand('copy');
        document.body.removeChild(dummy);
        xtalert.alertSuccessToast('复制成功');
    });

});