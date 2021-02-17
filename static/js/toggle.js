const toggleButton = document.getElementsByClassName('toggle-button')[0]
const navbarLinks1 = document.getElementsByClassName('navbar-links')[0]
const navbarLinks2 = document.getElementsByClassName('navbar-links')[1]
const navbarLinks3 = document.getElementsByClassName('navbar-links')[2]
const navbarLinks4 = document.getElementsByClassName('navbar-links')[3]


toggleButton.addEventListener('click', () => {
    navbarLinks1.classList.toggle('active')
})

toggleButton.addEventListener('click', () => {
    navbarLinks2.classList.toggle('active')
})

toggleButton.addEventListener('click', () => {
    navbarLinks3.classList.toggle('active')
})

toggleButton.addEventListener('click', () => {
    navbarLinks4.classList.toggle('active')
})

