$(function () {
    $('.hl-thread').click(function () {
        var self = $(this);
        var tr = self.parent().parent();
        var flag = self.attr('flag');
        var url = '';
        var thread_id = tr.attr('thread_id');
        if (flag == '1') {
            url = '/cms/dishl_thread/'
        } else if (flag == '2') {
            url = '/cms/hl_thread/'
        } else {
            url = '/cms/del_thread/'
        }

        xtalert.alertConfirm({
            title: '您确定要操作吗?',
            confirmCallback: function () {
                zlajax.post({
                    'url': url,
                    'data': {
                        'thread_id': thread_id
                    },
                    'success': function (data) {
                        if (data['code'] == 200) {
                            xtalert.alertSuccessToast('操作成功');
                            setTimeout(function () {
                                window.location = '/cms/thread/'
                            }, 500)
                        }
                    },
                    'fail': function () {
                        xtalert.alertNetworkError()
                    }
                })
            }
        });


    })
});