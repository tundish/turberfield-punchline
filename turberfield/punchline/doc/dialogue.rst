Dialogue
::::::::

Punchline files may consist simply of lines of text. However, for more advanced cases you can use these elements:

* `Field lists`_
* `Directives`_
* `Citations`_

Field lists
===========

Field lists are key/value pairs, in the format ``:key: value``.

Releasing content
-----------------

You can use field list metadata to control when pages are published. Four fields are available for that.
All are optional. All accept a date or timestamp string:

made_at:
    Captures the time you created the entry, eg: ``:made_at: 2020-08-29 14:16``

edit_at:
    Captures the time you last changed the entry, eg: ``:edit_at: 2020-08-29 10:03:22``

view_at:
    Specifies when you first want the entry to be seen, eg: ``:view_at: 2020-09-01``

drop_at:
    Specifies when you want the entry to be withdrawn, eg: ``:drop_at: 2020-09-30``

File naming
-----------

By default, Punchline names each HTML file after the second-level title which introduces the text.

Alternatively, you can opt for a numerically based name which is generated from the ordinal position of the text
in your dialogue. The `nodes` field takes a `format string`_ whose one argument is an integer.

.. code:: rest

    :nodes:     {0:02d}

Tags
----

You can use metadata to tag dialogue with whatever keywords you wish. You can add as many tags as you like
to the metadata, eg:

.. code:: rest

    :tag:   Python
    :tag:   Linux

.. todo:: Tag clouds are not yet implemented.

Feeds
-----

You can create multiple feeds for your site by adding ``:feed:`` attributes to the metadata.
Eg::

    :feed: poetry
    :feed: coding

Any dialogue without such attributes will appear in the *all* feed.

Presentation
------------

You can change the timing of the text animation. ``dwell`` is the time in seconds per word. ``pause`` is the
number of seconds delay after each delivered line::


    :dwell: 0.2
    :pause: 0.5

Directives
==========

Punchline supports all the directives_ provided by the Turberfield Dialogue library.
The ones you are likely to need are:

* Entity_
* Property_
* FX_

Entity
------

An entity declaration tells Punchline that there is a Python object it needs to be aware of.
There are two main cases where this is useful.

The object might be a speaker of dialogue. Punchline needs to know the speaker's name. So you declare
such an object to be `Eponymous` like this:

.. code:: rest

    .. entity:: ROSENCRANTZ
       :types: turberfield.punchline.types.Eponymous

This allows you to use the citations_ `[ROSENCRANTZ]_` to create spoken dialogue.

The other case is when you want access to Theme settings from the dialogue itself. Punchline will expose
a `Settings` object for you:

.. code:: rest

    .. entity:: SETTINGS
       :types: turberfield.punchline.types.Settings

Property
--------

A Property directive lets you access useful data held in Python objects. You can use those values in substitution
references, or you can modify them from your dialogue.

A good example of this is theme settings. Suppose you want to change the colours to suit some narrative mood.
You can set a value for a colour attribute like so:

.. code:: rest

    .. property:: SETTINGS.punchline-colour-midtone hsl(86, 93%, 12%, 0.7)

FX
--

Punchline will animate still images in the same manner it does text.
You can also play audio files. In both cases you use the `fx` directive:

.. code:: rest

    .. fx:: tor.static.img  tower.jpg
       :offset: 0
       :duration: 0

The first argument is the name of the package in which the resource is to be found. The second is the relative
file path to it. Punchline recognises different file suffixes and will render the media accordingly.

The `offset` and `duration` parameters are optional. They control the animation time of images in milliseconds.

Citations
---------

Punchline employs this core feature of reStructuredText_ as a way of representing a screenplay. So long as the
entity_ has been declared, you define character dialogue like this:

.. code:: rest

    [ROSENCRANTZ]_

        You have to ask questions.

You can use reStructuredText_ markup within dialogue for emphasis or to provide hyperlinks.

Example
=======

The following example is taken from ``questions.rst`` in the source repository.

.. include:: ../examples/questions.rst
    :literal:
    :code: rest

.. _reStructuredText: https://docutils.sourceforge.io/docs/user/rst/quickref.html
.. _directives: https://turberfield-dialogue.readthedocs.io/en/latest/syntax.html#elements
.. _format string: https://docs.python.org/3/library/string.html#formatstrings
