const delete_user_form = document.getElementById('delete-user')

delete_user_form.addEventListener('submit', async (event) => {
    event.preventDefault()

    const formData = new FormData(delete_user_form)
    const user_id = formData.get('user_id')

    const response = await fetch(`api/admin/delete_user/${user_id}`, {
        method: 'DELETE'
    })

    const data = await response.json()
    if (data.success) {
        delete_user_form.reset()
        alert('User was deleted')
    } else {
        alert(data.message)
    }
    console.log(data)
})