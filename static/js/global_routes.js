const logout_link = document.getElementById('logout-link')

logout_link.addEventListener('click', async (event) => {
    event.preventDefault()

    const response = await fetch('api/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })

    window.location.replace('/login')
})