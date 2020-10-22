Dialogue
::::::::

Field lists
===========


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

File naming
-----------

:nodes:     {0:02d}

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

Example
=======

The following example is taken from ``questions.rst`` in the source repository.

.. include:: ../examples/questions.rst
    :literal:
    :code: rest

.. _resRtucturedText: https://docutils.sourceforge.io/docs/user/rst/quickref.html
.. _directives: https://turberfield-dialogue.readthedocs.io/en/latest/syntax.html#elements
