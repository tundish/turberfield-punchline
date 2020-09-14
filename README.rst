Punchline
:::::::::

What worried me recently
++++++++++++++++++++++++

There aren't enough jokes on the web. I'd like to see more satire. Urgently.

There is indeed, on the web a lot of poetry. But poetry web sites are not poetic places. Or even happy spaces.

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

        Statement! One - Love.

    Second point
    ------------

    [ROSENCRANTZ]_

        Cheating!

    [GUILDENSTERN]_

        How?

    [ROSENCRANTZ]_

        I hadn't started yet.

    [GUILDENSTERN]_

        Statement! Two - Love.

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

        Three - Love and Game.

    .. _questions: https://en.wikipedia.org/wiki/Questions_(game)

Guide
=====

Punchline dialogue is written in reStructuredText_ and incorporates the extensions from the 
`Turberfield dialogue library`_.

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


Tags
----

You can use metadata to tag dialogue with whatever keywords you wish. You can add as many tags as you like
to the metadata, eg::

    :tag:   Python
    :tag:   Linux

Feeds
-----

You can create multiple feeds for your site by adding ``:feed:`` attributes to the metadata.
Eg::

    :feed: if
    :feed: coding

Any dialogue without such attributes will appear in the *all* feed.

Config file
-----------

The specifics of your published site (its URL for example) are controlled by a configuration file. You can
specify the file by using the ``--config`` option to the punchline tool (see below).

Punchline comes with a default configuration file which looks like this::

    [DEFAULT]
    site_title = My Punchline site
    site_url = /
    feed_title = Site Feed
    feed_name = all
    feed_url = ${site_url}feeds/${feed_name}.json

    [all]

This is the bare minimum you need to configure a feed for *all* category tags.

Copy this file and create a section for each feed category you want to publish.

You should edit the ``site_url`` variable in the ``[DEFAULT]`` section.
Change it to the URL of your live web site. Likewise with ``site_title``.

Themes
------

Punchline has a theme plug-in system which permits complete customisation of the rendered site, including if
necessary the JSON feed output.

The interface is still in development, and is not documented just now.

In the meantime, for rebranding and layout changes, please edit the local copy of *bfost.css* after your site
is rendered in the default theme.

Installation
============

These instructions assume:

    * a Python 3.8+ installation
    * a Windows terminal (`Git Bash`_ is recommended)

Linux and Mac users will need to adjust the execution path where necessary.

#. First make a virtual environment::

    python -m venv ~/py3-blog

#. Update the package manager within it::

    ~/py3-blog/Scripts/pip install -U pip, wheel

#. Download the `repository as a zip file <https://github.com/tundish/turberfield-punchline/archive/master.zip>`_

#. Install punchline::

    ~/py3-blog/Scripts/pip install turberfield-punchline-master.zip

#. Build a blog from the example dialogue::

    ~/py3-blog/Scripts/punchline.exe turberfield/punchline/examples/

#. Launch a local web server to view the site (`http://localhost:8000`)::

    ~/py3.8-blog/Scripts/python -m http.server -d turberfield/punchline/examples/output/

Further steps
=============

Read the options available when running ``punchline``::

    ~/py3-blog/Scripts/punchline.exe --help

.. _JSON Feed: https://jsonfeed.org/version/1.1
.. _web rings: https://www.mic.com/p/how-geocities-webrings-made-the-90s-internet-a-cozier-place-19638198
.. _web feeds: https://en.wikipedia.org/wiki/Web_feed
.. _Git Bash: https://gitforwindows.org/
.. _reStructuredText: https://docutils.sourceforge.io/rst.html
.. _Turberfield dialogue library: https://turberfield-dialogue.readthedocs.io/en/latest/
