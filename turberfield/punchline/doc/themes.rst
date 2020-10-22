Themes
::::::

Punchline has a theme plug-in system which permits complete customisation of the rendered site, including if
necessary the JSON feed output.

.. todo:: The interface is still in development, and is not documented just now.

    In the meantime, for rebranding and layout changes,
    please edit the local copy of **punchline.css** after your site is rendered in the default theme.

Settings
========

If all you need to change are the colours, you can achieve that with a modification to the configuration file.
Try adding the following section, and experimenting with the colour values::

    [theme]
    punchline-colour-washout = hsl(50, 0%, 100%, 1.0)
    punchline-colour-shadows = hsl(37, 93%, 12%, 0.7)
    punchline-colour-midtone = hsl(86, 93%, 12%, 0.7)
    punchline-colour-hilight = hsl(224, 70%, 16%, 0.7)
    punchline-colour-glamour = hsl(76, 80%, 35%, 1.0)
    punchline-colour-gravity = hsl(36, 20%, 18%, 1.0)

These and other settings can also be changed from within dialogue.
In particular, you can change ``punchline-states-refresh``, eg::

    .. property:: SETTINGS.punchline-states-refresh inherit

Possible values are as follows:

none
    No page refresh.
inherit
    The page refreshes to the next in the dialogue sequence. This is the default behaviour.
a URL
    Explicitly sets the next page to go to. In this way it is possible to create a
    `simple choice-based hypertext game`_ with Punchline.

Choosing themes
===============

In order to specify your chosen theme, add a ``theme`` option to the ``[DEFAULT]`` section of the
configuration file::

    theme = my_theme_module

Debugging
=========

In the event that you have hard-coded absolute URLs in your blog site, you'll find that breaks when you
develop with a local web server. There is a configuration option called ``site_mod`` you can use in this case.

Punchline will replace any instances of ``site_url`` with whatever you define in ``site_mod``. So to develop
locally::

    [theme]
    site_mod = /

.. _simple choice-based hypertext game: https://github.com/tundish/inimitable
