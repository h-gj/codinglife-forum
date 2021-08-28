/**
 * Created by Administrator on 2017/3/15.
 */

$(function () {
    $('#btn').click(function (event) {
        event.preventDefault();
        var oldpwdInput = $('input[name=old_pwd]');
        var newpwdInput = $('input[name=new_pwd]');
        var newpwdRepeatInput = $('input[name=new_pwd_repeat]');

        var old_pwd = oldpwdInput.val();
        var new_pwd = newpwdInput.val();
        var new_pwd_repeat = newpwdRepeatInput.val();

        zlajax.post({
           'url': '/cms/resetpwd/',
            'data': {
                'old_pwd': old_pwd,
                'new_pwd': new_pwd,
                'new_pwd_repeat': new_pwd_repeat
            },
            'success': function (data) {
                if(data['code'] == 200){
                    oldpwdInput.val('');
                    newpwdInput.val('');
                    newpwdRepeatInput.val('');
                    xtalert.alertSuccessToast('密码修改成功');
                }else{
                    xtalert.alertInfoToast(message);
                }
            },
            'fail': function (error) {
                // console.log(error);
                xtalert.alertNetworkError();
            }
        });
    });
});
