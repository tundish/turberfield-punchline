..  Titling
    ##++::==~~--''``

.. This is a reStructuredText file.

Change Log
::::::::::

0.4.0
=====

Extensive refactoring of the Theme class and public API.

* Created a Widget parent class to manage optional content.
* `dwell` and `pause` can be set from dialogue metadata.
* Removed the `--theme` option. It is now set in the default section
  of the config file.

0.3.0
=====

* Implemented theme overrides via property setters in .rst files.
* Added `--theme` option which accepts a theme name or module path.

0.2.0
=====

* Restyled the default theme.
* Implemented theme overrides from config file.

0.1.0
======

* First release.
