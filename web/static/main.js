const buttons=document.querySelectorAll(".btn")
buttons.forEach(function (button){
    button.addEventListener("click", function(element){
        const url = button.getAttribute("data-url")
        fetch(url)
    })
})