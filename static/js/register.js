form = document.getElementById('register-form')

form.addEventListener('submit', async (event) => {
    event.preventDefault()

    const formData = new FormData(form)

    const response = await fetch('/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(Object.fromEntries(formData)) // Turns formData into json object
    })

    const data = await response.json()
    if (data.success) {
        form.reset() // Clear inputs
        window.location.href = '/login'
    } else {
        alert(data.message)
    }
    console.log(data)
})