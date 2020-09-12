Punchline
:::::::::

.. note:: This code is pre-Release.

What worried me recently
++++++++++++++++++++++++

There aren't enough jokes on the web. We need more satire. Urgently.

There is indeed on the web a lot of poetry, but poetry web sites are not poetic places. Or even happy spaces.

Also the traditions of personal web sites, `web rings`_, and `web feeds`_ are no longer common practice.
And I felt sad about that.

What I did about it
+++++++++++++++++++

I wrote *Punchline*.

Punchline is a static blogging framework. It treats your words as speech, and delivers them as dialogue with
measured timing. It supports multimedia too.

Punchline was designed from the ground up to generate `JSON Feed`_. So you can publish your blog as a feed
under the topics you choose.

User Guide
++++++++++

Example
=======

If you want to see this example working on your PC, follow the steps for installation_ first.

.. code:: rest

    .. This is a comment. What follows is metadata

    :made_at: 2020-08-29
    :view_at: 2020-09-01
    :author:  Tom Stoppard

    .. Now we declare the voices used in the dialogue.

    .. entity:: ROSENCRANTZ
       :types: turberfield.punchline.types.Eponymous

    .. entity:: GUILDENSTERN
       :types: turberfield.punchline.types.Eponymous

    .. Dialogue scripts have a top-level title. Think of it as the name of a theatrical scene.

    The Game of Questions
    =====================

    .. Second-level titles represent shots in the scene. Here is the first of three.

    First point
    -----------

    [ROSENCRANTZ]_

        Do you want to play questions_?

    [GUILDENSTERN]_

        How do you play that?

    [ROSENCRANTZ]_

        You have to ask questions.

    [GUILDENSTERN]_

        Statement! One, Love.

    Second point
    ------------

    [ROSENCRANTZ]_

        Cheating!

    [GUILDENSTERN]_

        How?

    [ROSENCRANTZ]_

        I hadn't started yet.

    [GUILDENSTERN]_

        Statement! Two, Love.

    Third point
    -----------

    [ROSENCRANTZ]_

        Are you counting that?

    [GUILDENSTERN]_

        What?

    [ROSENCRANTZ]_

        Are you counting that?

    [GUILDENSTERN]_

        Foul! No repetitions.

        Three, Love and Game.

    .. _questions: https://en.wikipedia.org/wiki/Questions_(game)

Concepts
========

RestructuredText
----------------

Tags and feeds
--------------

Releasing content
-----------------

You can use metadata to control when pages are published. Four fields are available for that.
All are optional. All accept a date or timestamp string:

made_at:
    Captures the time you created the entry, eg: ``:made_at: 2020-08-29 14:16``

edit_at:
    Captures the time you last changed the entry, eg: ``:edit_at: 2020-08-29 10:03:22``

view_at:
    Specifies when you first want the entry to be seen, eg: ``:view_at: 2020-09-01``

drop_at:
    Specifies when you want the entry to be withdrawn, eg: ``:drop_at: 2020-09-30``


Config file
-----------

Punchline comes with a default configuration file which looks like this::

    [DEFAULT]
    site_url = /
    feed_title = Site Feed
    feed_name = all
    feed_url = ${site_url}feeds/${feed_name}.json

    [all]

This is the bare minimum you need to configure a feed for *all* category tags.


Themes
------

Installation
============

#. First make a virtual environment::

    python -m venv ~/py3-blog

#. Update the package manager within it::

    ~/py3-blog/Scripts/pip install -U pip, wheel

#. Install punchline::

    ~/py3-blog/Scripts/pip install turberfield-punchline-master.zip

#. Build a blog from the example dialogue::

    ~/py3-blog/Scripts/python -m turberfield.punchline.main turberfield/punchline/examples/

#. Launch a local web server to view the site (`http://localhost:8000`)::

    ~/py3.8-blog/Scripts/python -m http.server -d turberfield/punchline/examples/output/

.. _JSON Feed: https://jsonfeed.org/version/1.1
.. _web rings: https://www.mic.com/p/how-geocities-webrings-made-the-90s-internet-a-cozier-place-19638198
.. _web feeds: https://en.wikipedia.org/wiki/Web_feed
