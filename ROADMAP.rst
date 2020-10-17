..  Titling
    ##++::==~~--''``

.. This is a reStructuredText file.

Roadmap
:::::::

If you're reading this, it's because you are one of the first to discover Punchline_.

You are here during its initial few months. Here's what I'm planning to implement shortly:

Theme support
=============

From the beginning, Punchline has had a pluggable theme architecture. The theme interface
has been under heavy development, and is not documented yet. That is due to change in the
next few weeks.

Widgets
=======

Punchline themes have access to a catalogue of standard widgets.
You can use the configuration file to modify their settings, or deactivate them.
Here's the kind of thing I have in mind for the future:

* A Tag cloud
* Social media badges (Twitter, etc)
* Disqus integration

JSON Feed
=========

Punchline is built around the idea of generating a feed for content which can be
aggregated in a distributed manner.

But `JSON Feed`_ itself is a new technology, and there has not yet been an opportunity to
see how this would work in practice. So there's going to be some refinement of that.

Bug fixes
=========

If you'd like me to fix something specific, please `log an issue`_ and I'll make it a
priority.

.. _Punchline: https://pypi.org/project/turberfield-punchline/
.. _JSON Feed: https://jsonfeed.org/version/1.1
.. _log an issue: https://github.com/tundish/turberfield-punchline/issues

