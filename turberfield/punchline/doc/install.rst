Installation
::::::::::::

* Windows_
* Linux_

Windows
=======

Punchline is a very simple command line tool.
You use it from the Windows command interpreter.

To launch a new command window:

#. Tap the Windows key so that the Start Menu pops up.
#. Type the word `cmd`.
#. When you see the *Command Prompt* app highlighted, tap the Enter key.

You should see a prompt like this (your user name will differ)::

    Microsoft Windows [Version 10.0.18362.1139]
    (c) 2019 Microsoft Corporation. All rights reserved.

    C:\Users\author>

Prerequisites
-------------

Download and install Python from https://www.python.org/ .
Make sure to check the option to add `python` to your environment path.
This makes command line operation more easy.

After you've installed Python, open a command window and type `python`.
You should see something like this::

    C:\Users\author>python
    Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 22:45:29) [MSC v.1916 32 bit (Intel)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

Type `quit()` and press Return.

Virtual Environment
-------------------

#. First make a fresh Python virtual environment::

    python -m venv C:\Users\author\punchline-app

#. Update the package manager within it::

    C:\Users\author\punchline-app\Scripts\pip install -U pip, wheel

Install
-------

#. Download the `repository as a zip file <https://github.com/tundish/turberfield-punchline/archive/master.zip>`_.
   Unzip it to a local directory.

#. Install Punchline::

    C:\Users\author\punchline-app\Scripts\pip install turberfield-punchline-master.zip

Run
---

#. Build a blog from the example dialogue::

    C:\Users\author\punchline-app\Scripts\punchline.exe turberfield\punchline\examples

#. Launch a local web server to view the site (`http://localhost:8000`)::

    C:\Users\author\punchline-app\Scripts\python -m http.server -d turberfield\punchline\examples\output

Linux
=====

The Linux command line is generally more easy to work with than the Windows command prompt.
If you're finding the Windows command prompt tricky, you can install `Git Bash`_ which behaves in a
Linux-like way.

I encourage you to move to a Linux operating system when you are able. 
You can try one out at little cost on a `Raspberry Pi`_ or similar device.

Here are the install instructions for Linux.

Virtual Environment
-------------------

#. First make a fresh Python virtual environment::

    python3 -m venv ~/punchline-app

#. Update the package manager within it::

    ~/punchline-app/bin/pip install -U pip, wheel

Install
-------

#. Download the `repository as a zip file <https://github.com/tundish/turberfield-punchline/archive/master.zip>`_.
   Unzip it to a local directory.

#. Install Punchline::

    ~/punchline-app/bin/pip install turberfield-punchline-master.zip

Run
---

#. Build a blog from the example dialogue::

    ~/punchline-app/bin/punchline turberfield/punchline/examples/

#. Launch a local web server to view the site (`http://localhost:8000`)::

    ~/punchline-app/bin/python -m http.server -d turberfield/punchline/examples/output/


.. _JSON Feed: https://jsonfeed.org/version/1.1
.. _web rings: https://www.mic.com/p/how-geocities-webrings-made-the-90s-internet-a-cozier-place-19638198
.. _web feeds: https://en.wikipedia.org/wiki/Web_feed
.. _Git Bash: https://gitforwindows.org/
.. _reStructuredText: https://docutils.sourceforge.io/rst.html
.. _Turberfield dialogue library: https://turberfield-dialogue.readthedocs.io/en/latest/
.. _Raspberry Pi: https://www.raspberrypi.org/
