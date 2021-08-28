$(function () {
    $('#login').click(function (e) {
        e.preventDefault();
        var account = $('input[name="account"]').val();
        var password = $('input[name="password"]').val();
        var remember = $('input[name="remember"]').checked?1:0;

        zlajax.post({
           'url': '/login/',
           'data': {
               'account': account,
               'password': password,
               'remember': remember
           },
            'success': function (data) {
                if (data['code'] == 200){
                    var next_to = $('#next_to').text();
                    window.location = next_to
                } else {
                    $('.alert-container').removeClass('hidden');
                    $('.strong').text(data['message'])
                }
            },
            'fail': function () {
                xtalert.alertNetworkError()
            }
        });
    });
});