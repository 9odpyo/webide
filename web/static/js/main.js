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
        $('#python-result-area').val($('#python-result-area').val() + data.line)
    });
});

function runPythonCode(){
    var formData = new FormData();
    var pythonCode = $('#python-code-area').val();
    console.log(pythonCode)
    formData.append('pythonCode', pythonCode);

    $.ajax({
        url : '/runPythonCode',
        type : 'POST',
        data : formData,
        processData: false,  // tell jQuery not to process the data
        contentType: false,  // tell jQuery not to set contentType
        success : function(data) {
            $('#python-result-area').val('');
            socket.emit('join_result', {'rid': '111', 'file_path': data.file_path})
        },
        error : function(data) {
             alert("fail...");
        }
    });
}
