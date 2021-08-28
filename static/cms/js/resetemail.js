$(function () {
   $('#send-btn').click(function (event) {
       event.preventDefault();
       var email = $('#email').val();
        if (!email){
            xtalert.alertInfoToast('请输入邮箱');
            return
        }
       zlajax.get({
           'url': '/cms/sendcaptcha/',
           'data': {
               'email': email
           },
           'success': function (data) {
               if (data['code'] == '200'){
                   xtalert.alertInfoToast('验证码发送成功');
               }else{
                   var message = data['message'];
                   xtalert.alertInfo(message)
               }
           },
           'fail': function () {
               xtalert.alertNetworkError()
           }
       })
   });
});

$(function () {
   $('#submit').click(function (e) {
       e.preventDefault();
       var emailE = $('#email');
       var captchaE = $('input[name="captcha"]');

       var email = emailE.val();
       var captcha = captchaE.val();

       zlajax.post({
           'url': '/cms/resetemail/',
           'data': {
               'email': email,
               'captcha': captcha
           },
           'success': function (data) {
             if (data['code'] == 200){
                 emailE.val('');
                 captchaE.val('');
                 xtalert.alertInfoToast('邮箱修改成功')
             }else{
                 msg = data['message'];
                 xtalert.alertInfo(msg)
             }
           },
           'fail': function () {
               xtalert.alertNetworkError()
           }
       });
   });
});