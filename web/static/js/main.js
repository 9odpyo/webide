var socket;
$(document).ready(function(){
    var namespace = '/ide-py';
    socket = io(namespace)
    socket.on('connect', function() {
        socket.emit('handshake', {data: 'hello'});
    });
    socket.on('join_result', function(data) {
        socket.emit('get_result', {'rid': data.rid, 'file_path': data.file_path})
    });
    socket.on('get_result', function(data) {
        $('#result-area').val($('#result-area').val() + data.line)
    });

    const $elNavLink = $('.nav-link');
    $elNavLink.click((e) => {
        $elNavLink.removeClass('active');
        $(e.target).addClass('active');
    });
});

function runCode(){
    var formData = new FormData();
    var code = $('#code-area').val();
    var language = $('.nav-link.active').data('language');
    console.log(code)
    console.log(language)
    formData.append('code', code);
    formData.append('language', language);

    $.ajax({
        url : '/runCode',
        type : 'POST',
        data : formData,
        processData: false,  // tell jQuery not to process the data
        contentType: false,  // tell jQuery not to set contentType
        success : function(data) {
            $('#result-area').val('');
            socket.emit('join_result', {'rid': '111', 'file_path': data.file_path})
        },
        error : function(data) {
             alert("fail...");
        }
    });
}
