let markup = `
    <style>
        .content {
            width: 100%;
            height: 100%;
            display: flex;
        }
        .content .item {
            padding: 10px;
            font-family: Arial;
        }
        .content .item .close_btn {
            border: 0;
        }
    </style>
    <div class="content"></div>
`

let item = document.createElement("div")
item.innerHTML = `
<span class="name"></span>
<button class="close_btn">×</button>
`
item.className = "item"

class Tabs extends HTMLElement {
    #shadow = null
    #content = null
    constructor(){
        super()
        this.attachShadow({mode:"open"})
        this.shadowRoot.innerHTML = markup
        this.#content = this.shadowRoot.querySelector(".content")
    }
    addTab(name,data){
        let i = item.cloneNode(true)
        i.querySelector(".name").innerHTML = name
        i.data = data
        this.#content.appendChild(i)
    }
    clear(){
        this.#content.innerHTML=""
    }
    get count(){
        return this.shadowRoot.querySelector(".content").children.length
    }
}

customElements.define("tabs-view",Tabs)
