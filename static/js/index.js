const logout_button = document.getElementById('logout-button')



logout_button.addEventListener('click', async (event) => {
    event.preventDefault()

    const response = await fetch('api/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })

    window.location.href = '/login'
})