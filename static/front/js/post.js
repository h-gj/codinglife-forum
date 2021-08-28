$(function () {
    var ue = UE.getEditor('container', {
        'serverUrl': '/ueditor/upload/'
    });

    var pubBtn = $('#publish-btn');
    pubBtn.click(function (e) {
        e.preventDefault();
        var tid = $(this).attr('tid');
        var titleE = $('input[name="title"]');
        var content = ue.getContent();
        var board_id = $('select[name="board"]').val();

        zlajax.post({
            'url': '/thread/',
            'data': {
                'title': titleE.val(),
                'content': content,
                'board_id': board_id,
                'tid': tid
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    xtalert.alertConfirm({
                        'title': tid ? '更新成功' : '发表成功',
                        'confirmText': '再发一遍',
                        'cancelText': '回到首页',
                        'confirmCallback': function () {
                            titleE.val('');
                            ue.setContent('')
                        },
                        'cancelCallback': function () {
                            window.location = '/'
                        }
                    })
                } else {
                    xtalert.alertInfo(data['message'])
                }
            },
            'fail': function () {
                xtalert.alertNetworkError()
            }

        })
    });

    $('input[name="title"]').val($('#title').html());
    var bid = $('#board').text();
    $('option[value="'+bid+'"]').attr('selected', 'true');
    ue.ready(function () {
        ue.setContent($('#content').html());
    });
    pubBtn.attr('flag', 'mod');
});