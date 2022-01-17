let token = localStorage.getItem("tooen")
if(!token){
    location = "/login?from="+ encodeURI(location)
}
