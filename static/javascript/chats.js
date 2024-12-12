let usersDataDivElement = document.getElementById('users-data');
let userId = usersDataDivElement.getAttribute('data-user-id');
let targetUserId = usersDataDivElement.getAttribute('data-target-user-id');

messagesUrl = 'http://localhost:8000/chats/messages/' + `${userId}/${targetUserId}/`;
let last_messages = null;

document.addEventListener('DOMContentLoaded', async () => {
    let messagesResponse = await fetch(messagesUrl);
    last_messages = await messagesResponse.json();
})

async function checkRefreshPage() {
    let messagesResponse = await fetch(messagesUrl)
    let messagesData = await messagesResponse.json()
    let are_messages_equal = JSON.stringify(messagesData) === JSON.stringify(last_messages)

    if (!are_messages_equal) {
        location.reload();
    }
}

setInterval(checkRefreshPage, 3000);
