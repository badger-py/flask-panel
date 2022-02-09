import "./pager.js"

let tables = document.querySelector("#tables");
tables = (() => {
    let temp = []
    for(let node of tables.childNodes.values()){
	if(node.nodeType != node.COMMENT_NODE)continue;
	temp.push(node.nodeValue);
    }
    return temp
})();
alert(tables)
