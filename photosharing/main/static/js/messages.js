const id = JSON.parse(document.getElementById('json-username').textContent);
const message_username = JSON.parse(document.getElementById('json-message-username').textContent);
const my_id = document.getElementById('id_user_sender').value;

console.log(message_username)

const socket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/'
    + id
    + '/'
    + my_id
    + '/'
);

socket.onopen = function(e){
    console.log("CONNECTION ESTABLISHED");
}

socket.onclose = function(e){
    console.log("CONNECTION LOST");
}

socket.onerror = function(e){
    console.log("ERROR OCCURED");
}

socket.onmessage = function(e){
    const data = JSON.parse(e.data);
    const now = new Date();
    const date = now.toLocaleDateString('en-GB', { dateStyle: 'medium' });
    const time = now.toLocaleTimeString('en-GB', { timeStyle: 'short' });

    if(data.username == message_username){
        document.querySelector('#chat-body').innerHTML += `
            <tr>
                <td style="float: right;">
                <p class="bg-success p-2 mt-2 mr-5 shadow-sm text-white float-right rounded">${data.message}</p>
                </td>
                <td>
                    <p><small class="p-1 shadow-sm">${date},${time}</small>
                    </p>
                </td>
            </tr>`
    }else{
        document.querySelector('#chat-body').innerHTML += `
            <tr>
                <td style="float: left;">
                <p class="bg-primary p-2 mt-2 mr-5 shadow-sm text-white float-left rounded">${data.message}</p>
                </td>
                <td style="float: left;">
                    <p><small class="p-1 shadow-sm">${date},${time}</small>
                    </p>
                </td>
            </tr>`
    }
}

document.querySelector('#chat-message-submit').onclick = function(e){
    const message_input = document.querySelector('#message_input');
    const message = message_input.value;

    socket.send(JSON.stringify({
        'message':message,
        'username':message_username
    }));

    message_input.value = '';
}