$(function () {
    $('.comment-del-btn').click(function (e) {
        e.preventDefault();
        var comment_id = $(this).attr('comment_id');
        xtalert.alertConfirm({
            title: '确定删除吗',
            confirmCallback: function () {
                zlajax.post({
                    'url': '/cms/del_comment/',
                    'data': {
                        'comment_id': comment_id
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            xtalert.alertSuccessToast('删除成功');
                            setTimeout(function () {
                                window.location = '/cms/comment/'
                            }, 500)
                        } else {
                            xtalert.alertInfo(data['message'])
                        }
                    },
                    'fail': function () {
                        xtalert.alertNetworkError()
                    }
                })
            }
        });
    });
});