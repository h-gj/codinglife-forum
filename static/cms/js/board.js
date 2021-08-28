$(function () {
   $('#add-board').click(function (e) {
       e.preventDefault();
       xtalert.alertOneInput({
           'title': '添加板块',
           'placeholder': '请输入板块名称',
           'confirmCallback': function (inputValue) {
               zlajax.post({
                   'url': '/cms/add_board/',
                   'data': {
                       'name': inputValue
                   },
                   'success': function (data) {
                       if (data['code'] == 200){
                           xtalert.alertInfoToast('添加成功');
                           window.location.reload()
                       } else{
                           xtalert.alertInfo(data['message'])
                       }
                   },
                   'fail': function () {
                       xtalert.alertNetworkError()
                   }
               })
           }
       });
   });

   $('.modify-board').click(function (e) {
       e.preventDefault();
       var bdid = $(this).attr('bdid');
       xtalert.alertOneInput({
           'title': '修改板块',
           'placeholder': $(this).parent().siblings().eq(0).text(),
           'confirmCallback': function (inputValue) {
               zlajax.post({
                   'url': '/cms/mod_board/',
                   'data': {
                       'name': inputValue,
                       'bdid': bdid
                   },
                   'success': function (data) {
                       if (data['code'] == 200){
                           xtalert.alertSuccessToast('修改成功');
                           setTimeout(function () {
                               window.location = '/cms/board/'
               }, 700)
                       } else{
                           xtalert.alertInfo(data['message'])
                       }
                   },
                   'fail': function () {
                       xtalert.alertNetworkError()
                   }
               });
           }
       });
   });


    $('.delete-board').click(function (e) {
       self  = $(this);
       e.preventDefault();
       xtalert.alertConfirm({
           'title': '删除板块',
           confirmCallback: function () {
               var bdid = self.attr('bdid');
               zlajax.post({
                   'url': '/cms/del_board/',
                   'data': {
                       'bdid': bdid
                   },
                   'success': function (data) {
                       if (data['code'] == 200) {
                           window.location.reload()
                       } else {
                           xtalert.alertInfo(data['message'])
                       }
                   },
                   'fail': function () {
                       xtalert.alertNetworkError()
                   }
               });
           }
       });
   });
});
