$(function () {
   $('#btn').click(function (e) {
       e.preventDefault();
       var old_pwd_E = $("input[name=old_pwd]");
       var new_pwd_E = $('input[name=new_pwd]');
       var confirm_E = $('input[name=new_pwd_repeat]');

       var old_pwd = old_pwd_E.val();
       var new_pwd = new_pwd_E.val();
       var new_pwd_repeat = confirm_E.val();

       zlajax.post({
           'url': '/cms/resetpwd/',
           'data': {
               'old_pwd': old_pwd,
               'new_pwd': new_pwd,
               'new_pwd_repeat': new_pwd_repeat
           },
           'success': function (data) {
               if (data['code'] == 200){
                   xtalert.alertInfoToast('修改成功');
                   old_pwd_E.val("");
                   new_pwd_E.val("");
                   confirm_E.val("");
               }else{
                   error = data['message'];
                   xtalert.alertInfo(error);
               }
           },
           'fail': function (error) {
               xtalert.alertNetworkError();
           }
       });
   });
});