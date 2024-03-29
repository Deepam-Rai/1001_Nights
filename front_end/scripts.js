// constants;
const INPUT_TEXT = "input-text"
const INPUT_OVERLAY = "input-overlay"
const INFO_TEXT = "info-text"
const CONTINUE_STORY_BTN = "continue-story-btn"
const SERVER_URL = "http://localhost:5005/webhooks/rest/webhook"
const DEFAULT = "default"
const NO_BOT_UTTER = "no_bot_utter"
const INFO_MSGS = {
    [DEFAULT]: "Oops! Something went wrong. Please try again later."
}


!(function () {
    /**
     * Handles the chat message box.
     * Addition of message box on load up.
     * Also handles user and bot messages for the message box.
     */
    let e = document.createElement("script"),
        t = document.head || document.getElementsByTagName("head")[0];
    (e.src =
        "https://cdn.jsdelivr.net/npm/rasa-webchat/lib/index.js"),
        (e.async = !0),
        (e.onload = () => {
            window.WebChat.default(
                {
                    customData: { language: "en" },
                    socketUrl: "http://localhost:5005",
                    title: '1001',
                    subtitle: '',
                    // add other props here
                },
                null
            );
        }),
        t.insertBefore(e, t.firstChild);
})();


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
async function sendUserMessage(input) {
    /**
     * input: str, is whatever payload to be sent to the rasa backend.
     * This function wraps this payload and sends to rasa backend.
     * The response is jsonized and returned.
     */
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify({
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
        const response = await fetch("http://localhost:5005/webhooks/rest/webhook", requestOptions);
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
        response = await sendUserMessage(tillNow);
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