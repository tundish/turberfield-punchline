# This file is part of turberfield.
#
# Turberfield is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Turberfield is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with turberfield.  If not, see <http://www.gnu.org/licenses/>.

import functools

from turberfield.dialogue.model import Model

class Renderer:

    @staticmethod
    def animated_audio_to_html(anim):
        return f"""<div>
    <audio src="/audio/{anim.element.resource}" autoplay="autoplay"
    preload="auto" {'loop="loop"' if anim.element.loop and int(anim.element.loop) > 1 else ""}>
    </audio>
    </div>"""


    @staticmethod
    def animated_line_to_html(anim):
        return f"""
    <li style="animation-delay: {anim.delay:.2f}s; animation-duration: {anim.duration:.2f}s">
    <blockquote class="obj-line">
    <header class="{'obj-persona' if hasattr(anim.element.persona, '_name') else 'obj-entity'}">
    { '{0.firstname} {0.surname}'.format(anim.element.persona.name) if hasattr(anim.element.persona, 'name') else ''}
    </header>
    <p class="obj-speech">{ anim.element.html }</p>
    </blockquote>
    </li>"""


    @staticmethod
    def animated_still_to_html(anim):
        return f"""
    <div style="animation-duration: {anim.duration}s; animation-delay: {anim.delay}s">
    <img src="/img/{anim.element.resource}" alt="{anim.element.package} {anim.element.resource}" />
    </div>"""


    @staticmethod
    def render_frame_to_html(frame, ensemble=[], title="", final=False):
        heading = " ".join("<span>{0}</span>".format(i.capitalize()) for i in title.split(" "))
        dialogue = "\n".join(Renderer.animated_line_to_html(i) for i in frame[Model.Line])
        stills = "\n".join(Renderer.animated_still_to_html(i) for i in frame[Model.Still])
        audio = "\n".join(Renderer.animated_audio_to_html(i) for i in frame[Model.Audio])
        return f"""
    {audio}
    <section class="fit-banner">
    <h1>{heading}</h1>
    </section>
    <aside class="fit-gallery">
    {stills}
    </aside>
    <div class="fit-speech">
    <main>
    <ul class="obj-dialogue">
    {dialogue}
    </ul>
    </main>
    <nav>
    <ul>
    <li><form role="form" action="/" method="GET" name="contents">
    {'<button action="submit">Home</button>' if final else ''}
    </form></li>
    </ul>
    </nav>
    </div>"""


    @staticmethod
    def render_frame_to_text(frame, ensemble=[], title="", final=False):
        return "\n".join(
            ["{0}{1}{2}".format(
                " ".join(filter(None, anim.element.persona.name)) if hasattr(anim.element.persona, "name") else "",
                ": " if hasattr(anim.element.persona, "name") else "",
                anim.element.text
            ) for anim in frame[Model.Line]]
        )


    @staticmethod
    def render_feed_to_html(pages, root, config=None):
        heading = " ".join(
            "<span>{0}</span>".format(i)
            for i in config.defaults()["site_title"].split(" ")
        ) if config else ""
        feed_list = "\n".join(
            '<li><a href="{0}{1}">{2}</a></li>'.format(
                config.defaults()["site_url"] if config else "",
                page.path.relative_to(root).as_posix(),
                page.title.title()
            )
            for page in pages
            if not page.ordinal
        )
        return f"""
    <section class="fit-banner">
    <h1>{ heading }</h1>
    </section>
    <div class="fit-speech">
    <main>
    <ul>
    { feed_list }
    </ul>
    </main>
    <nav>
    <ul>
    </ul>
    </nav>
    </div>"""


    @staticmethod
    def render_dict_to_css(mapping=None, tag=":root"):
        mapping = mapping or {}
        entries = "\n".join("--{0}: {1};".format(k, v) for k, v in mapping.items())
        return f"""{tag} {{
    {entries}
    }}"""


    @staticmethod
    @functools.lru_cache()
    def render_body_html(title="", refresh=None, next_=""):
        return f"""<!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {'<meta http-equiv="refresh" content="{0};/{1}">'.format(refresh, next_) if refresh and next_ else ''}
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>{title}</title>
    <link rel="stylesheet" href="/css/bfost.css" />
    {{0}}
    </head>
    <body>
    <style type="text/css">
    {{1}}
    </style>
    {{2}}
    </body>
    </html>"""


