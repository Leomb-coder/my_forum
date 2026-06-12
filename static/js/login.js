form = document.getElementById('login-form')

form.addEventListener('submit', async (event) => {
    event.preventDefault()

    const formData = new FormData(form)

    const response = await fetch('api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(Object.fromEntries(formData))
    })

    const data = await response.json()
    if (data.success) {
        form.reset()
    }
    console.log(data)
})