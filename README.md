Corthus is under construction
===========

This is a web application I created during my master thesis. 
Now I defended the thesis, so I can finally turn the project 
into something useful (if only I have time for this).
And then, hopefully, this page will also contain some reasonable 
description of the project. For now, the best you can get is
the [master thesis][1] (only in Polish).

Here are some screenshots:

![screenshot](//raw.github.com/mik01aj/corthus/master/doc/web2.png)
![screenshot](//raw.github.com/mik01aj/corthus/master/doc/websearch.png)

To make the current version work you need to do:

    virtualenv .
    . bin/activate
    easy_install django
    ln -s ../../../corthus/toolkit lib/python2.7/site-packages/toolkit

And then you can start the server:

    cd corthus_web/
    ./manage.py runserver

See you soon!

[1]: https://github.com/mik01aj/corthus/blob/master/doc/magisterka.pdf?raw=true
