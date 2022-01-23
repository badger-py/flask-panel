window.onload = e => {
    let form = document.querySelector("form");
    form.addEventListener("submit",e => {
        e.preventDefault();
        let xhr = new XMLHttpRequest();
        xhr.onload = ()=>{
            alert(`${xhr.status} ${xhr.statusText}`);
            console.log(xhr)
        };
        xhr.onerror = () => {
            
        };
        xhr.open("POST","/login",true);
        xhr.setRequestHeader("Content-Type", "application/json");
        
        xhr.send(JSON.stringify({
            user:form.elements["user"].value,
            pass:form["pass"].value,
            remember:form["remember"].checked
        }));
    },true)
}