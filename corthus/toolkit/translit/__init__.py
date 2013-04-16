
"""
This package contains various transliteration functions.

@author m01
"""

from expand_cu import expand_cu, multi_replace
from render_cu import render_cu
from cu2pl import cu2pl
#from cu2en import cu2en
from el2pl import el2pl

from hip2unicode import hip2unicode

from simplify_el import simplify_el

from metaphone import metaphone, metaphone_text, detect_language


def translit_pl(text, lang):
    assert lang in ('pl', 'cu', 'el')
    if lang == 'pl':
        return text
    elif lang == 'cu':
        return cu2pl(expand_cu(text))
    else:
        return el2pl(simplify_el(text))
