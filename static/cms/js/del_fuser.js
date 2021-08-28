$(function () {
    $('.comment-del-btn').click(function () {
        var uid = $(this).attr('user_id');
        zlajax.get({
            'url': '/cms/del_fuser/?uid=' + uid,
            'success': function (data) {
                if (data['code'] == 200) {
                    xtalert.alertConfirm({
                        title: '确定删除吗',
                        confirmCallback: function () {
                            xtalert.alertSuccessToast('删除成功');
                            setTimeout(function () {
                                window.location.reload()
                            }, 600)
                        }
                    });
                }
            },
            'fail': function () {
                xtalert.alertNetworkError()
            }
        })
    });
});
