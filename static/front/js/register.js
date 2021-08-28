$(function () {
    $('#capcha-img').click(function (e) {
        var self = $(this);
        var src = self.attr('src');
        var newSrc = param.setParam(src, 'r', Math.random());
        self.attr('src', newSrc)
    });
});

$(function () {
    $('#send_sms').click(function (e) {
        e.preventDefault();
        var self = $(this);
        var email = $('input[name="email"]').val();
        zlajax.get({
            'url': '/cms/sendcaptcha/?email=' + email,
            'success': function (data) {
                if (data['code'] == 200) {
                    $('.alert-container').removeClass('hidden');
                    $('.strong').text('邮箱验证码发送成功');
                    var count = 60;
                    self.attr('disabled', 'disabled');
                    var timer = setInterval(function () {
                        self.text(count + 's');
                        count--;
                        if (count <= 0) {
                            self.removeAttr('disabled');
                            self.text('发送验证码');
                            clearInterval(timer);
                        }
                    }, 1000)
                } else {
                    $('.alert-container').removeClass('hidden');
                    $('.strong').text(data['message'])
                }
            },
            'fail': function () {
                xtalert.alertNetworkError()
            }
        })
    });
});

$(function () {
    $('#sub-btn').click(function (e) {
        e.preventDefault();
        // var phone = $('input[name="phone"]').val();
        var email = $('input[name="email"]').val();
        var captcha = $('input[name="captcha"]').val();
        var username = $('input[name="username"]').val();
        var password1 = $('input[name="password1"]').val();
        var password2 = $('input[name="password2"]').val();
        var img_captcha = $('input[name="img_captcha"]').val();
        var next_to = $('#next_to').text();
        zlajax.post({
            'url': '/register/',
            'data': {
                // 'phone': phone,
                'email': email,
                'captcha': captcha,
                'username': username,
                'password1': password1,
                'password2': password2,
                'img_captcha': img_captcha,
            },
            'success': function (data) {
                if (data['code'] == 200) {
                    xtalert.alertSuccessToast('注册成功');
                    setTimeout(function () {
                        window.location = next_to
                    }, 500)
                } else {
                    $('.alert-container').removeClass('hidden');
                    $('.strong').text(data['message'])
                }
            },
            'fail': function () {
                $('.alert-container').removeClass('hidden');
                $('.strong').text('网络错误')
            }
        });
    });
});