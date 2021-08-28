$(function () {
    $('.item-info-div').hover(function () {
        $(this).addClass('hover');
    }, function () {
        $(this).removeClass('hover')
    });

    $('.remove-item').click(function (e) {
        e.preventDefault();
        var iid = $(this).attr('iid');
        xtalert.alertConfirm({
            title: '您确定删除吗？',
            confirmCallback: function () {
                zlajax.get({
                    url: '/delitem/?iid=' + iid,
                    success: function (data) {
                        if (data['code'] === 200) {
                            window.location.reload()
                        } else {
                            xtalert.alertError('删除失败')
                        }
                    }
                })
            }
        })

    })
});

