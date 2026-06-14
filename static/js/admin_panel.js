// const delete_user_form = document.getElementById('delete-user')
const create_forum_form = document.getElementById('create-forum')
const ban_user_form = document.getElementById('ban-user')
const unban_user_form = document.getElementById('unban-user')

// delete_user_form.addEventListener('submit', async (event) => {
//     event.preventDefault()
//
//     const formData = new FormData(delete_user_form)
//     const user_id = formData.get('user_id')
//
//     const response = await fetch(`api/admin/delete_user/${user_id}`, {
//         method: 'DELETE'
//     })
//
//     const data = await response.json()
//     if (data.success) {
//         delete_user_form.reset()
//         alert('User was deleted')
//     } else {
//         alert(data.message)
//     }
//     console.log(data)
// })

// Create Forum
create_forum_form.addEventListener('submit', async (event) => {
    event.preventDefault()

    const formData = new FormData(create_forum_form)
    const slug = formData.get('forum-slug')

    const response = await fetch('api/admin/create_forum', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(Object.fromEntries(formData))
    })

    const data = await response.json()

    if (data.success) {
        create_forum_form.reset()
        window.location.href = `/forum/${slug}`
        alert('Forum was created')
    } else {
        alert(data.message)
    }
    console.log(data)
})

// Ban User
ban_user_form.addEventListener('submit', async (event) => {
    event.preventDefault()

    const formData = new FormData(ban_user_form)

    const response = await fetch('api/admin/ban_user', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(Object.fromEntries(formData))
    })

    const data = await response.json()

    if (data.success) {
        ban_user_form.reset()
        alert('User was banned')
    } else {
        alert(data.message)
    }
    console.log(data)
})

unban_user_form.addEventListener('submit', async (event) => {
    event.preventDefault()

    const formData = new FormData(unban_user_form)

    const response = await fetch('api/admin/unban_user', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(Object.fromEntries(formData))
    })

    const data = await response.json()

    if (data.success) {
        ban_user_form.reset()
        alert('User was unbanned')
    } else {
        alert(data.message)
    }
    console.log(data)
})