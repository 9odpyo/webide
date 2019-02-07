var socket;
var namespace = '/ide-pyo';
var CODE_TYPE_PYTHON = 'python';
var CODE_TYPE_JAVA = 'java';
var CODE_TYPE_SHELL = 'shell';
var CODE_TYPE_JAVASCRIPT = 'js';
var samplePythonCode = "import time\n\nprint('test - {} - god - {}'.format('!!', str(2**5)))\ntime.sleep(1)\nprint('wait 1second')\ntime.sleep(2)\nprint('wait 2second')\nprint('aba')";
var sampleShellCode = "#!/bin/bash\n\nRAW_TIMESTAMP=$(date +\"%Y-%m-%d %H\")\nRAW_TIMESTAMP=$(date -d \"$RAW_TIMESTAMP\" +%s)\n\necho \"time : $RAW_TIMESTAMP\"\nsleep 1\necho \"done\""

$(document).ready(function(){
    initTypeSelectButton();
    initSocket();
});

function initTypeSelectButton(){
    $('#code-area').val(samplePythonCode);
    $('.type-select_button').on('click', function(){
        $('.type-select_button').removeClass('active');
        $(this).addClass('active');
        var codeType = this.dataset.codeType;
        $('#code-type').val(codeType);
        if(codeType == CODE_TYPE_PYTHON){
            $('#code-area').val(samplePythonCode);
        } else if(codeType == CODE_TYPE_JAVA){
            $('#code-area').val(sampleShellCode);
        } else if(codeType == CODE_TYPE_SHELL){
            //TODO sample java code
        } else if(codeType == CODE_TYPE_JAVASCRIPT){
            //TODO sample js code
        }
    });
}

function initSocket(){
    socket = io(namespace)
    socket.on('connect', function() {
        socket.emit('handshake', {data: 'hello'});
    });
    socket.on('join_result', function(data) {
        var codeType = $('#code-type').val();
        socket.emit('get_result', {'rid': data.rid, 'file_path': data.file_path, 'code_type': codeType})
    });
    socket.on('get_result', function(data) {
        $('#result-area').val($('#result-area').val() + data.line)
    });
}

function runCode(){
    var formData = new FormData();
    var codeType = $('#code-type').val();
    var codeText = $('#code-area').val();
    formData.append('codeType', codeType);
    formData.append('codeText', codeText);

    console.log(codeType);
    console.log(codeText);

    $.ajax({
        url : '/runCode',
        type : 'POST',
        data : formData,
        processData: false,
        contentType: false,
        success : function(data) {
            $('#result-area').val('');
            socket.emit('join_result', {'rid': '111', 'file_path': data.file_path})
        },
        error : function(data) {
             alert("fail...");
        }
    });
}
