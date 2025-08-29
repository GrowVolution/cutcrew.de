function connectSocket() {
    const domain = "wss://cutcrew.de";
    return io(domain, {
        transports: ['websocket'],
        reconnection: true,
        reconnectionAttempts: 5,
        reconnectionDelay: 1000,
        reconnectionDelayMax: 5000,
        timeout: 20000
    })
}

let socket = connectSocket();

function emit(event, data=null) {
    socket.emit('default_event', {
        event: event,
        payload: data
    })
}

let htmlEventHandler
function defaultHtmlHandler(block) {
    function handleHtml(html) {
        if (block) {
            block.innerHTML = html;
            const scripts = block.querySelectorAll('script');
            scripts.forEach(script => {
                eval(script.innerText);
            })
        } else console.log('Error - HTML Block not found!');
    }
    return handleHtml;
}
socket.on('html', (html) => { htmlEventHandler(html) })


let requestSuccessHandler
socket.on('success', (data) => { requestSuccessHandler(data) })


socket.on('flash', (data) => {
    flash(data['msg'], data['cat']);
})

socket.on('error', (message) => {
    console.log(message);
    showInfo("Socket Fehler", "Beim Ausführen der Aktion ist ein Fehler aufgetreten.\n" +
        `Fehler Nachricht: "${message}". Wende dich bitte an developer@growv-mail.org um diesen Fehler zu melden.`);
})