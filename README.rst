Punchline
:::::::::

What worried me recently
========================

There aren't enough jokes on the web. We need more satire. Urgently.

There is indeed on the web a lot of poetry, but poetry web sites are not poetic places. Or even happy spaces.

And the traditions of personal web sites, `web rings`_, and `web feeds`_ are no longer common practice.

What I did about it
===================

I wrote *Punchline*.

Punchline is a static blogging framework. It treats your words as speech, and delivers them as dialogue with
measured timing. It supports multimedia too.

Punchline was designed from the ground up to generate `JSON Feed`_. So you can publish your blog as a feed
under the topics you choose.

Installation
============

#. First make a virtual environment::

    python -m venv ~/py3-blog

#. Update the package manager within it::

    ~/py3-blog/Scripts/pip install -U pip, wheel

#. Install punchline::

    ~/py3-blog/Scripts/pip install turberfield-punchline-master.zip


.. _JSON Feed: https://jsonfeed.org/version/1.1
.. _web rings: https://www.mic.com/p/how-geocities-webrings-made-the-90s-internet-a-cozier-place-19638198
.. _web feeds: https://en.wikipedia.org/wiki/Web_feed
