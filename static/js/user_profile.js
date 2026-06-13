const pfp_form = document.getElementById('change-profile-picture')

pfp_form.addEventListener('submit', async (event) => {
    event.preventDefault()

    const formData = new FormData(pfp_form)

    const response = await fetch('api/change_user_picture', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(Object.fromEntries(formData))
    })

    const data = await response.json()
    if (data.success) {
        pfp_form.reset()
        location.reload()
    } else {
        alert(data.message)
    }

    console.log(data)
})