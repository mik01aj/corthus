
$(document).ready(
   function() {

      var mapped = {};
      var textarea = document.getElementById('corrections');
      var active_checkbox = document.getElementById('match-radio');

      active_checkbox.checked = true;

      function set_selection(lang, num, status, className) {
         className = (typeof className !== 'undefined') ? className : 'selected';
         console.log(lang + "-" + num + " " + status);
         if (status) /* select */
            document.getElementById(lang + "-" + num).classList.add(className);
         else /* deselect */
            document.getElementById(lang + "-" + num).classList.remove(className);
      }

      $("tr .sentence").click(
         function() {
            if (!active_checkbox.checked)
               return;
            var id_s = this.id.split('-');
            var clicked_lang = id_s[0];
            var clicked_num = id_s[1];
            if (clicked_lang in mapped)
               set_selection(clicked_lang, mapped[clicked_lang], false);
            mapped[clicked_lang] = clicked_num;
            set_selection(clicked_lang, clicked_num, true);
         });

      $(document).keyup(
         function(event) {
            if (!active_checkbox.checked)
               return;
            /* console.log(event.keyCode); */
            if (event.keyCode == 27) { /* esc */
               for (i in langs) {
                  var selected_num = mapped[langs[i]];
                  set_selection(langs[i], selected_num, false);
               }
               mapped = {};
               return;
            }
            if (event.keyCode != 13) /* not enter */
               return;
            var rung_str = '';
            for (i in langs) {
               var selected_num = mapped[langs[i]];
               rung_str += selected_num + "\t";
               set_selection(langs[i], selected_num, false);
               set_selection(langs[i], selected_num, true, 'selected2');
            }
            textarea.value += rung_str + "0";

            /* sorting rows */
            var sortfun = function(x, y) { return parseInt(x)-parseInt(y); };
            textarea.value = textarea.value.split('\n').sort(sortfun).join('\n');

            textarea.value += '\n';
         });

      /* console.log("Hello"); */
   });
