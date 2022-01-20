let cookies = Object.create(null)

export let Cookies = {
    get(name){
	if(name in cookies)return cookies[name];
	else null;
    },
    set(name, val){
	
    }
}
