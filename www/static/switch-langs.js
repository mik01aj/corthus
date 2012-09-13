
langs = langs.split('-'); /* languages currently shown */

var f = function() {
   var option_inputs = document.getElementById('options').getElementsByTagName('input');
   console.log(langs);
   for (var i=0; i<option_inputs.length; i++) {
      var cbox = option_inputs[i];
      cbox.checked = (langs.indexOf(cbox.value) != -1);
   }

   $("#options input").change(function() {
      var values = [];
      for (var i=0; i<option_inputs.length; i++) {
         if (option_inputs[i].checked)
            values.push(option_inputs[i].value);
      }
      var new_langs = values.join('-'); /* new selected languages */
      setCookie('langs', new_langs, 30);
      if (reload_page_on_change) {
         document.getElementById('options-progress').style.visibility = 'visible';
         var loc = ("" + document.location).split('.');
         loc.pop();
         loc.push(new_langs);
         window.location = loc.join('.');
      }
   });

   /* console.log("Hello"); */

}

$(document).ready(f);
