..  Titling
    ##++::==~~--''``

.. This is a reStructuredText file.

Change Log
::::::::::

0.7.0
=====

* Fixed a bug in creating Eponymous classes.
* Fixed a bug in rendering widgets.
* Fixed the path used by feed from config.
* Added `site_mod` mechanism to optionally modify URLs.

0.6.0
=====

* `Raw` HTML declarations are now permitted in dialogue.
* The setting `punchline-states-refresh` may now be a URL.

0.5.0
=====

* Added a simpler banner font; Tenderness.
* Fixed a bug with the default config file.
* Fixed a bug with theme module search paths.

0.4.0
=====

Extensive refactoring of the Theme class and public API.

* Created a Widget parent class to manage optional content.
* `dwell` and `pause` can be set from dialogue metadata.
* Removed the `--theme` option. It is now set in the default section
  of the config file.
* Namespaced the variables used in styling themes.
* Added a `nodes` metadata field to control frame naming.
* Added the `punchline-states-refresh` setting to control inter-frame refresh.

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
