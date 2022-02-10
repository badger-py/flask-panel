import "./tabs.js";

let markup = `
    <style>
	    .tabs {
            width: 100%;
        }
    </style>
    <div>
	<tabs-view class="tabs"></tabs-view>
	<div class="contents"><slot name=""></slot></div>
    </div>
`;


class Pager extends HTMLElement {
    #shadow = null
    #observer = null
    #tabs = null
    #slot = null
    constructor(){
	    super()
	    this.#observer = new MutationObserver(this.mutationCallback.bind(this))
        this.#observer.observe(this,{
            childList:true,
            attributes:true
        })
        this.attachShadow({mode:"open"})
        this.shadowRoot.innerHTML = markup
        this.#slot = this.shadowRoot.querySelector("slot")
        this.#tabs = this.shadowRoot.querySelector(".tabs")
    }
    mutationCallback(mutations){
        console.log(mutations)
	    for(let mut of mutations){
            if(mut.type == "childList"){
                for(let del of mut.removedNodes){
                    this.removeTab(del)
                }
                for(let added of mut.addedNodes){
                    this.addTab(added.name || "untitled", added)
                }
            }
        }
    }
    connectedCallback(){
        if (this.#tabs.count != this.children.length) {
            this.#tabs.clear()
            for (const elem of this.children) {
                this.addTab(elem.getAttribute("name") || "untitled",elem)
            }
        }
    }
    removeTab(el){
        
    }
    addTab(name,el){
        if (el.parentElement != this) {
            this.appendChild(el)
        }
        this.#tabs.addTab(name||"untitled",{el})
    }
}

customElements.define("panel-pager", Pager)
