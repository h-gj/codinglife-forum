$(function () {
    $('.buser-del-btn').click(function () {
        var self = $(this);
        var uid = self.attr('user_id');
        zlajax.delete({
            url: '/cms/buser/?uid=' + uid,
            success: function (data) {
                if (data['code'] === 200) {
                    self.parent().parent().remove();
                } else {
                    xtalert.alertError(data['message'])
                }
            }
        })
    });

    var uid = '';

    $('.buser-mod-btn').click(function () {
        var self = $(this);
        uid = self.attr('user_id');
    });
    var usernameE = $('input[name="name"]');
    var emailE = $('input[name="email"]');
    var passwordE = $('input[name="password"]');
    var roleE = $('select option:selected');

    $('#save').click(function (e) {
        e.preventDefault();
        var self = $(this);
        var username = usernameE.val();
        var email = emailE.val();
        var password = passwordE.val();
        var role_id = roleE.val();

        zlajax.post({
            'url': '/cms/buser/',
            'data': {
                'username': username,
                'email': email,
                'password': password,
                'role_id': role_id,
            },
            'success': function (data) {
                if (data['code'] === 200) {
                    window.location.reload();
                } else {
                    xtalert.alertInfo(data['message'])
                }
            },
            'fail': function () {
                xtalert.alertNetworkError()
            }
        });

    });

    $('#save-change').click(function (e) {
        e.preventDefault();
        var self = $(this);
        var role_id = $('select[name="change-role"] option:selected').val();

        zlajax.put({
            'url': `/cms/buser/?uid=${uid}&role_id=${role_id}`,
            'success': function (data) {
                if (data['code'] === 200) {
                    window.location.reload();
                } else {
                    xtalert.alertInfo(data['message'])
                }
            },
            'fail': function () {
                xtalert.alertNetworkError()
            }
        });

    });
});