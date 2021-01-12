const displayAll = (elts, display) => {
    elts.forEach(elt => {
        if (display) {
            elt.style.display = "block"
        } else {
            elt.style.display = "none"
        }
    })
}

const toggleElt = elt => {
    const display = elt.style.display
    if (display === "none") {
        elt.style.display = "block"
    } else {
        elt.style.display = "none"
    }
}

// Hide english text, show japanese by default
const enText = document.querySelectorAll("p[class^=en]")
displayAll(enText, false)

const jpText = document.querySelectorAll("p[class^=jp]")
displayAll(jpText, true)

// When clicking on the button, switch between the two languages
const switchButtons = document.querySelectorAll("button[class^=switch-lang]")
switchButtons.forEach(btn => {
    btn.addEventListener("click", () => {
        // Extract number from class
        const idx = btn.className.match(/\d+/)[0]

        const enElt = document.querySelector(`.en-${idx}`)
        const jpElt = document.querySelector(`.jp-${idx}`)

        toggleElt(enElt)
        toggleElt(jpElt)
    })
})

// Switch between the two languages for all lines
document.getElementById("show-jp").addEventListener("click", e => {
    e.preventDefault()
    displayAll(jpText, true)
    displayAll(enText, false)
})

document.getElementById("show-en").addEventListener("click", e => {
    e.preventDefault()
    displayAll(jpText, false)
    displayAll(enText, true)
})
