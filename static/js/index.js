const logout_link = document.getElementById('logout-link')
const profile_link = document.getElementById('profile-link')

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

profile_link.addEventListener('click', async (event) => {
    event.preventDefault()

    window.location.href = '/profile'
})