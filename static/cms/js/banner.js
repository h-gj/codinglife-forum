$(function () {

    var nameE = $('input[name="name"]');
    var img_urlE = $('input[name="img_url"]');
    var link_urlE = $('input[name="link_url"]');
    var priorityE = $('input[name="priority"]');

    $('#banner-add-btn').click(function (e) {
        $('#save').attr('type', '');
        nameE.val('');
        img_urlE.val('');
        link_urlE.val('');
        priorityE.val('');
    });

   $('#save').click(function (e) {
       e.preventDefault();
       var self = $(this);
       var name = nameE.val();
       var img_url = img_urlE.val();
       var link_url = link_urlE.val();
       var priority = priorityE.val();

       var bid = self.attr('bid');
       var type = self.attr('type');
       var url = '';
        if (type){
            url = '/cms/mod_banner/';
        } else {
            url = '/cms/add_banner/'
        }
       zlajax.post({
           'url': url,
           'data': {
               'name': name,
               'img_url': img_url,
               'link_url': link_url,
               'priority': priority,
               'bid': bid
           },
           'success': function (data) {
               if (!name || !img_url || !link_url || !priority){
                   return
               }
               if (data['code'] == 200){
                   if (bid){
                       xtalert.alertSuccessToast('修改成功');
                   } else {
                       xtalert.alertSuccessToast('添加成功');
                   }
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


   $('.modify-btn').click(function (e) {
       e.preventDefault();
       var self = $(this);
       var tr = self.parent().parent();

       var name = tr.attr('bname');
       var img_url = tr.attr('bimg_url');
       var link_url = tr.attr('blink_url');
       var priority = tr.attr('bpriority');
       var bid = tr.attr('bid');

       nameE.val(name);
       img_urlE.val(img_url);
       link_urlE.val(link_url);
       priorityE.val(priority);

       var save = $('#save');
       save.attr('type', 'modify');
       save.attr('bid', bid);
   });


   $('.del-btn').click(function (e) {
       self  = $(this);
       e.preventDefault();
       xtalert.alertConfirm({
           'title': '温馨提示',
           'msg': '确定删除吗',
           confirmCallback: function () {
               var trE = self.parent().parent();
               var bid = trE.attr('bid');
               zlajax.post({
                   'url': '/cms/del_banner/',
                   'data': {
                       'bid': bid
                   },
                   'success': function (data) {
                       if (data['code'] == 200) {
                           xtalert.alertSuccessToast('删除成功');
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
           }
       });
   });
});
