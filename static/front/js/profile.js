$(function () {
    $('#save').click(function (e) {
        e.preventDefault();
        var username = $('#username').val();
        var user_id = $('#username').attr('user_id');
        var phone = $('#phone').val();
        var email = $('#email').val();
        var qq = $('#qq').val();
        var gender = $('#gender').val();
        var old_pwd = $('#old_pwd').val();
        var new_pwd = $('#new_pwd').val();

        zlajax.post({
            'url': '/updateprofile/' + user_id + '/',
            'data': {
                'username': username,
                'phone': phone,
                'email': email,
                'qq': qq,
                'gender': gender,
                'old_pwd': old_pwd,
                'new_pwd': new_pwd
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    xtalert.alertSuccessToast('修改成功');
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

    $('#image').change(function () {
        var image = $('#image').get(0).files[0];
        var form_data = new FormData();
        form_data.append('avatar', image);
        console.log(form_data);
        zlajax.post({
            url: '/qiniuupload/',
            data: form_data,
            contentType: false,
            processData: false,
            success: function (data) {
                if (data['code'] == 200) {
                    xtalert.alertSuccessToast('上传成功');
                    setTimeout(function () {
                        window.location.reload()
                    }, 600)
                } else {
                    xtalert.alertInfoToast(data['message'])
                }
            },
            fail: function () {
                xtalert.alertNetworkError()
            }
        });
    })
});
