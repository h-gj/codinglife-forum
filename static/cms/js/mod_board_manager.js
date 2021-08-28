$(function () {
    var usernameE = $('input[name="username"]');
    var boardE = $('input[name="board"]');
    usernameE.val('');
    boardE.val('');

    var bdid = null;
    var bdname = '';

    $('.board-manager-add-btn').click(function () {
        bdid = $(this).attr('bdid');
        bdname = $(this).attr('bdname');
        boardE.val(bdname);
    });

    $('.save-board-manage-btn').click(function (e) {
        e.preventDefault();
        var self = $(this);
        var username = usernameE.val();
        console.log('useranme', username);
        console.log('bdid', bdid);

        zlajax.post({
            'url': '/cms/board_manager/',
            'data': {
                'username': username,
                'bdid': bdid
            },
            'success': function (data) {
                console.log(data);
                if (data['code'] == 200) {
                    xtalert.alertSuccessToast('添加成功');
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
        });

    });


    var boardManagerName = $('.board-manager-name');
    var style = {'background-color': 'rgba(217,83,79,0.76)', 'font-size': 18, 'border-radius': '3px', 'padding': '5px'};
    boardManagerName.hover(function () {
        $(this).css(style);
        $(this).append(`<span class="badge board-manage-del-btn" style="cursor: pointer">x</span>`);
    }, function () {
        $(this).removeAttr('style');
        $(this).children().remove();
    });

    // TODO
    // $('.board-manage-del-btn').click(function (e) {
    //     var bmid = $(this).parent().attr('bmid');
    //     console.log('bmid', bmid);
    // });

    boardManagerName.click(function (e) {
        var bmid = $(this).attr('bmid');
        xtalert.alertConfirm({
            title: '您确定要取消该版主吗？',
            confirmCallback: function () {
                zlajax.delete({
                    'url': `/cms/board_manager/?bmid=${bmid}`,
                    'success': function (data) {
                        if (data['code'] === 200) {
                            $('span[bmid="' + bmid + '"]').remove();
                        } else {
                            xtalert.alertInfo(data['message'])
                        }
                    }
                })
            }
        });


    });
});
