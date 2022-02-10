let markup = `
    <style>
        .content {
            width: 100%;
            height: 100%;
            display: flex;
        }
        .content .item {
            
        }
    </style>
    <div class="content"></div>
`

let item = document.createElement("div")
item.innerHTML = `
<span class="name"></span>
<button class="close_btn"></button>
`

class Tabs extends HTMLElement {
    #shadow = null

    constructor(){
        super()
        this.#shadow = this.attachShadow({mode:"closed"})
        this.#shadow = markup
    }
    addTab(name,data){
        let i = item.cloneNode(true)
        i.querySelector(".name").innerHTML = name
        i.data = data
        this.#shadow.querySelector(".content").appendChild(i)i
        
    }
}

customElements.define("tabs-view",Tabs)
