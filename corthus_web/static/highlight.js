
function updateHighlight(parent_tr, rung_class, status) {
   var className = "highlight";
   var span_nodes = parent_tr.getElementsByTagName('span');
   for (var i=0; i<span_nodes.length; i++) {
      var node = span_nodes[i];
      console.log(node.id, node.classList, rung_class);
      if (node.classList && node.classList.contains(rung_class)) {
         console.log('ok');
         if (status) /* select */
            node.classList.add(className);
         else /* deselect */
            node.classList.remove(className);
      }
   }
}

function findParent(node, wanted_tag) {
   /* XXX may loop */
   var parent = node;
   while (parent.tagName.toLowerCase() != wanted_tag)
      parent = parent.parentNode;
   return parent;
}

$(document).ready(function() {

   $("tr .sentence").mouseover(function() {
      var rung_class = this.className.split(" ")[1];
      var parent_tr = findParent(this, "tr");
      updateHighlight(parent_tr, rung_class, true);
   });

   $("tr .sentence").mouseout(function() {
      var rung_class = this.className.split(" ")[1];
      var parent_tr = findParent(this, "tr");
      updateHighlight(parent_tr, rung_class, false);
   });

   /* console.log("Hello"); */
});
