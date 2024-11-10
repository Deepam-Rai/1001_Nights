// constants;
const INPUT_TEXT = "input-text"
const INPUT_OVERLAY = "input-overlay"
const INFO_TEXT = "info-text"
const CONTINUE_STORY_BTN = "continue-story-btn"
const SERVER_HOST = "http://localhost"
const CORE_RASA_SERVER= SERVER_HOST + ":5005"
const RASA_REST_ENDPOINT = CORE_RASA_SERVER + "/webhooks/rest/webhook"
const DEFAULT = "default"
const NO_BOT_UTTER = "no_bot_utter"
const INFO_MSGS = {
    [DEFAULT]: "Oops! Something went wrong. Please try again later."
}
STORY_CHAT_SENDER_ID = "story_chat"
SIDE_CHAT_SENDER_ID = "side_chat"
USER = "user"
BOT = "bot"


window.onload = function () {
    /*
        Clears local storage everytime page is refreshed.
        websocket connection for story chat
        websocket connection for side chat
    */
    localStorage.clear();
    initiate_story_chat();
    initiate_side_chat();
};


// --------------------------------------------------------------------
// side-chat code
let side_socket;
function initiate_side_chat() {
    /* Establishes side-chat conversation with rasa server
    */
    side_socket = io(CORE_RASA_SERVER);
    side_socket.on('connect', function (){
        STORY_CHAT_SENDER_ID = side_socket.id
        console.log("side-chat: Connected side chat conversation sender_id:" + SIDE_CHAT_SENDER_ID);
        side_socket.emit("user_uttered", {
            "message": "/greet",
            "sender_id": SIDE_CHAT_SENDER_ID
        });
        console.log("side-chat: Sent initiation message.")
    })
    side_socket.on('connect_errors', function (){
        console.error("side-chat: Error connecting side chat conversation.");
    })
    side_socket.on('bot_uttered', function(data) {
        const botMessage = data.text;
        appendMessageToChat(botMessage, 'bot');
        if (data.story_update) {
            data = data.story_update;
            console.log("Story update from side-chat:", data);
            toggleGenInput(false);
            document.getElementById(INPUT_TEXT).value += " " + data.alter_story + data.add_story + data.response;
            setInputTextHeight();
            toggleGenInput(true);
        }
    });
}


document.getElementById('chat-input').addEventListener('keypress', function(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();  // Prevent new line when only Enter is pressed; but allow shift+enter for newline
        sendSideMessage();  // Send message
    }
});


function sendSideMessage() {
    /*
        Sends side-chat user message to bot.
        Appends the user message to chat messages
    */
    const inputField = document.getElementById("chat-input");
    const chatMessages = document.getElementById("chat-messages");

    // Extract the message text
    const messageText = inputField.value.trim();

    // Check if the message is not empty
    if (messageText !== "") {
        // emit the message to rasa server
        side_socket.emit('user_uttered', {
            "message": messageText,
            "sender_id": SIDE_CHAT_SENDER_ID
        });
        appendMessageToChat(messageText, USER);
    }
}


function appendMessageToChat(message, sender) {
    const chatMessages = document.getElementById('chat-messages');  // Reference to the chat messages container

    // Create a new div to represent the message
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('chat-message', sender);
    messageDiv.textContent = message;

    chatMessages.appendChild(messageDiv);

    if (sender === USER) {
        document.getElementById("chat-input").value = ""
    }

    // Scroll to the bottom of the chat container to show the latest message
    chatMessages.scrollTop = chatMessages.scrollHeight;
}


// --------------------------------------------------------------------
// story-chat code

function initiate_story_chat() {
    const socket = io(CORE_RASA_SERVER);
    socket.on('connect', function (){
        STORY_CHAT_SENDER_ID = socket.id
        console.log("Connected story chat conversation sender_id:" + STORY_CHAT_SENDER_ID);
    })
    socket.on('connect_errors', function (){
        console.error("Error connecting story chat conversation.");
    })
}

function setInputTextHeight(height = null) {
    /**
     * height = null  -> Set as much height as required for the input size.
     * Input text field height changes dynamically with input size.
     * This function lets us do that.
     */
    const inputText = document.getElementById(INPUT_TEXT);
    inputText.style.height = (height == null) ? `${inputText.scrollHeight}px` : height;
}
function onInput(input) {
    /**
     * Handles what is to be done when user inputs a data on the input field.
     */
    setInputTextHeight()
    handleNewAddition(this);
}
function handleNewAddition(input) {
}
function setInputTextReadOnly(flag) {
    document.getElementById(INPUT_TEXT).readOnly = flag
}
let genInputs = true; // enabled/disabled state for inputs related to story generation
function toggleGenInput(flag = null) {
    /**
     * flag = true  -> Inputs are enabled.
     *      = false -> inputs are disabled.
     *      = null  -> Input state is toggled.
     * The whole area is also covered by overlay.
     * */
    genInputs = (flag == null) ? !(genInputs) : flag;
    setInputTextReadOnly(!genInputs)
    document.getElementById(CONTINUE_STORY_BTN).disabled = !genInputs
    document.getElementById(INPUT_OVERLAY).style.display = genInputs ? "none" : "flex"
}
async function sendStoryMessage(input, sender=STORY_CHAT_SENDER_ID) {
    /**
     * REST POST request for story-chat.
     * input: str, is whatever payload to be sent to the rasa backend.
     * This function wraps this payload and sends to rasa backend.
     * The response is jsonized and returned.
     */
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({
        "sender": sender,
        "message": input.trim(),
        "metadata": {}
    });
    console.log(raw)
    var requestOptions = {
        method: 'POST',
        headers: myHeaders,
        body: raw,
        redirect: 'follow'
    };
    try {
        const response = await fetch(RASA_REST_ENDPOINT, requestOptions);
        const result = await response.json();
        console.log("Bot response: ", result)
        return result;
    } catch (error) {
        console.error('Error: ', error);
        throw error;
    }
}
async function continueStory() {
    /**
     * Activates when user clicks on continue story button.
     * Sends the whole input in the input-text to rasa backend.
     * On receiving response, appends it to the input-text.
     * Triggers intent "continue_story" and fills the slot "till_now" in rasa.
     * If some issue rises, then also activates the "showInfo" field.
     */
    toggleGenInput(false)
    document.getElementById(INFO_TEXT).style.visibility = "hidden"
    let tillNow = document.getElementById(INPUT_TEXT).value
    tillNow = '/continue_story{"till_now":"' + tillNow + '"}'
    try {
        response = await sendStoryMessage(tillNow, sender=STORY_CHAT_SENDER_ID);
        if (response.length > 0) {
            bot_utter = await response[0]["text"]
            document.getElementById(INPUT_TEXT).value += " " + bot_utter
            setInputTextHeight()
            toggleGenInput(true)
        } else {
            showInfo(info_id = NO_BOT_UTTER)
            toggleGenInput(true)
        }
    } catch (error) {
        console.error('Error: ', error);
        toggleGenInput(true)
        throw error;
    }
}
function showInfo(info_id = DEFAULT, custom = null) {
    /**
     * info_id = Any key from dictionary "INFO_MSGS" declared at the starting.
     * custom = null  -> shows default info message.
     *        = something else -> Shows that as info message.
     * show-info is a div that shows infos, warnings, errors, etc to the user.
     * This function handles that div.
     */
    info_msg = ""
    if (custom != null) {
        info_msg = INFO_MSGS
    } else if (info_id in INFO_MSGS) {
        info_msg = INFO_MSGS[info_id]
    } else {
        info_msg = INFO_MSGS[DEFAULT]
    }
    infoText = document.getElementById(INFO_TEXT)
    console.log("New info: ", info_msg)
    infoText.innerHTML = info_msg
    infoText.style.visibility = "visible"
}