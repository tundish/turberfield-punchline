Themes
::::::

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

Config
======

::

    [DEFAULT]
    theme = my_theme_module
    .
    .
    .

    [theme]
    site_mod = /

Settings
========

::

    .. property:: SETTINGS.punchline-states-refresh inherit
