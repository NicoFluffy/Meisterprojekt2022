const buttons=document.querySelectorAll(".btn")
buttons.forEach(function (button){
    button.addEventListener("click", async function(element){
        button.disabled = true
        const url = button.getAttribute("data-url")
        await fetch(url)
        button.disabled = false
    })
})