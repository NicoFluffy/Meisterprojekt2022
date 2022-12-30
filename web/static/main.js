const buttons=document.querySelectorAll(".btn-click")
buttons.forEach(function (button){
    button.addEventListener("click", async function(element){
        button.disabled = true
        const url = button.getAttribute("data-url")
        await fetch(url)
        button.disabled = false
    })
})

const holdbuttons = document.querySelectorAll(".btn-hold")
holdbuttons.forEach(function (button){
    const richtung = button.getAttribute("data-richtung")
    button.addEventListener('contextmenu', event => event.preventDefault());

    const sendeRichtung = (richtung) => {
        fetch("/bewegung/" + richtung)
    }

    button.addEventListener("mousedown", () => sendeRichtung(richtung))
    button.addEventListener("mouseup", () => sendeRichtung(0))
    button.addEventListener("cancel", ()=> sendeRichtung(0))
    button.addEventListener("mouseleave", ()=> sendeRichtung(0))

    button.addEventListener("touchstart", () => sendeRichtung(richtung))
    button.addEventListener("touchend", ()=> sendeRichtung(0))
    button.addEventListener("touchcancel", ()=>  sendeRichtung(0))
})


document.querySelector("#vol").addEventListener("change", (e)=> {
    fetch("/vol/" + e.target.value)
})