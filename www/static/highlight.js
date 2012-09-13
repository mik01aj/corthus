
var highlight_color = '#ffa';

function updateHighlight(parent_tr, rung_class, color) {
   var span_nodes = parent_tr.getElementsByTagName('span');
   for (var i=0; i<span_nodes.length; i++) {
      var node = span_nodes[i];
      if (node.className &&
          node.className.split(" ").indexOf(rung_class) != -1) {
         node.style.backgroundColor = color;
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
      updateHighlight(parent_tr, rung_class, highlight_color);
   });

   $("tr .sentence").mouseout(function() {
      var rung_class = this.className.split(" ")[1];
      var parent_tr = findParent(this, "tr");
      updateHighlight(parent_tr, rung_class, '');
   });

   /* console.log("Hello"); */
});
