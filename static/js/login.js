window.onload = () => {
    let form = document.querySelector("form");
    form.addEventListener("submit",e => {
        e.preventDefault();
        let xhr = new XMLHttpRequest();
	xhr.responseType = "json"
        xhr.onload = ()=>{
            if(xhr.response && xhr.response.status == "ok"){
		location = "/"
	    } else {
		alert(xhr.responseText)
	    }
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
