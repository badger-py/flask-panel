import "./tabs.js";

let markup = `
    <style>
	    .tabs {
            width: 100%;
        }
    </style>
    <div>
	<div class="tabs"><tabs-view></tabs-view></div>
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
	    this.#shadow = this.attachShadow({mode:"closed"})
        this.#shadow.innerHTML = markup
        this.#slot = this.#shadow.querySelector("slot")
	    this.#observer = new MutationObserver(this.mutationCallback)
        this.#tabs = document.createElement("tabs-view");
    }
    mutationCallback(mutations){
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
    removeTab(el){
        
    }
    addTab(name,el){
        this.#tabs.addTab()
    }
}

customElements.define("panel-pager", Pager)
