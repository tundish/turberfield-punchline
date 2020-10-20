..  Titling
    ##++::==~~--''``

Overview
::::::::


The config file
===============

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

Presentation
------------

You can change the timing of the text animation. ``dwell`` is the time in seconds per word. ``pause`` is the
number of seconds delay after each delivered line::


    :dwell: 0.2
    :pause: 0.5

Config file
-----------

The specifics of your published site (its URL for example) are controlled by a configuration file. You can
specify the file by using the ``--config`` option to the punchline tool (see below).

Punchline comes with a default configuration file which looks like this::

    [DEFAULT]
    site_title = Your Blog Name Here
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

In the meantime, for rebranding and layout changes, please edit the local copy of *punchline.css* after your site
is rendered in the default theme.

If all you need to change are the colours, you can achieve that with a modification to the *.cfg* file.
Try adding the following section, and experimenting with the colour values::

    [theme]
    punchline-colour-washout = hsl(50, 0%, 100%, 1.0)
    punchline-colour-shadows = hsl(37, 93%, 12%, 0.7)
    punchline-colour-midtone = hsl(86, 93%, 12%, 0.7)
    punchline-colour-hilight = hsl(224, 70%, 16%, 0.7)
    punchline-colour-glamour = hsl(76, 80%, 35%, 1.0)
    punchline-colour-gravity = hsl(36, 20%, 18%, 1.0)

