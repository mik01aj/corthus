
$(document).ready(
   function() {

      var mapped = {};
      var textarea = document.getElementById('corrections');
      var active_checkbox = document.getElementById('correction-active');

      active_checkbox.checked = true;

      function set_selection(lang, num, status, className) {
         className = (typeof className !== 'undefined') ? className : 'selected';
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

      $(document).keypress(
         function(event) {
            if (!active_checkbox.checked)
               return;
            if (event.which != 13) /* enter */
               return;
            var rung_str = '';
            for (i in langs) {
               var selected_num = mapped[langs[i]];
               rung_str += selected_num + "\t";
               set_selection(langs[i], selected_num, false);
               set_selection(langs[i], selected_num, true, 'selected2');
            }
            textarea.value += rung_str + "\n";
         });

      /* console.log("Hello"); */
   });
