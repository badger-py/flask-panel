let markup = `
    <style>
	
    </style>
    <div>
	<div class="tabs"></div>
	<div class="contents"><slot name=""></slot></div>
    </div>
`;


class Pager extends HTMLElement {
    #shadow = null
    #observer = null
    constructor(){
	super()
	this.#shadow = this.attachShadow({mode:"closed"})
	this.#observer = new MutationObserver(this.mutationCallback)
    }
    mutationCallback(mutations){
	
    }
}

customElements.define("panel-pager", Pager)
