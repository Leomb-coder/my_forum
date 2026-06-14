// const delete_user_form = document.getElementById('delete-user')
const create_forum_form = document.getElementById('create-forum')

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