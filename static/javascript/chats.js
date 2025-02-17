let usersDataDivElement = document.getElementById('users-data');
let userId = usersDataDivElement.getAttribute('data-user-id');
let targetUserId = usersDataDivElement.getAttribute('data-target-user-id');

messagesUrl = 'http://localhost:8000/chats/messages/' + `${userId}/${targetUserId}/`;
let lastMessages = null;

document.addEventListener('DOMContentLoaded', async () => {
    let messagesResponse = await fetch(messagesUrl);
    lastMessages = await messagesResponse.json();
})

async function checkRefreshPage() {
    let messagesResponse = await fetch(messagesUrl)
    let messagesData = await messagesResponse.json()
    let are_messages_equal = JSON.stringify(messagesData) === JSON.stringify(lastMessages)

    if (!are_messages_equal) {
        location.reload();
    }
    lastMessages=messagesData
}

setInterval(checkRefreshPage, 5000);
