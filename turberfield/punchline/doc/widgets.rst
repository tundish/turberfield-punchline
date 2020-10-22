Widgets
:::::::

A Widget is a small component which a Punchline theme uses to render certain content.

Examples are tag clouds, social media badges, etc.

You can modify the behaviour of widgets from the configuration file.
By convention, the section names for widgets have *dotted* names, to denote the service they provide.
In some cases, removing the section from the configuration file will remove the widget entirely.

Here is an example of the configuration for the widget that renders the Punchline project web badge::

    [turberfield.punchline]
    url = https://pypi.org/project/turberfield-punchline/
    src = ${site_url}assets/punchline_icon-512x512.svg
    alt = A small icon of a cartoon sock puppet
    text = Powered by Punchline
    height = 48
    width = 48
