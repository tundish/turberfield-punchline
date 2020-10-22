..  Titling
    ##++::==~~--''``

Overview
::::::::

With Punchline, you write your blog content as a set of plain text files.

Plain text, but actually in a clever format called `reStructuredText`_.
With *.rst* files you can include metadata, hyperlinks and mark up text for emphasis.

Example
=======

Let's start with a bit of poetry. Below is a simple scrap of verse, which you will find in `marina.rst` in
the examples directory.


.. code:: rest

    :author: T. S. Eliot

    :dwell: 0.1
    :pause: 1.5

    Marina
    ======

    1
    -

    What seas what shores what grey rocks and what islands

    What water lapping the bow

    And scent of pine and woodthrush singing through the fog

    What images return

    O my daughter.

At the top, above the main content you can see some metadata about the file. Then there is the title.
There are two levels of titling in every Punchline file. The first is the title of the whole piece.
Second level titling creates individual pages. Here there is only one page.

The config file
===============

The other component of your Punchline blog is the configuration (*.cfg*) file.
 
The specifics of your published site (its URL for example) are controlled by this configuration file. You can
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

.. _reStructuredText: https://docutils.sourceforge.io/docs/user/rst/quickref.html
