import functools

from turberfield.dialogue.model import Model

def animated_audio_to_html(anim):
    return f"""<div>
<audio src="/audio/{anim.element.resource}" autoplay="autoplay"
preload="auto" {'loop="loop"' if anim.element.loop and int(anim.element.loop) > 1 else ""}>
</audio>
</div>"""


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


def animated_still_to_html(anim):
    return f"""
<div style="animation-duration: {anim.duration}s; animation-delay: {anim.delay}s">
<img src="/img/{anim.element.resource}" alt="{anim.element.package} {anim.element.resource}" />
</div>"""


def location_to_html(locn, path="/"):
    return f"""
<form role="form" action="{path}hop" method="post" name="{locn.id.hex}" >
    <input id="hop-{locn.id.hex}" name="location_id" type="hidden" value="{locn.id.hex}" />
    <button type="submit">{locn.label}</button>
</form>"""


def ensemble_to_html(ensemble, spots=None, here=False):
    narrator = ensemble[-1]
    spots = spots or [i.get_state(Spot) for i in ensemble if not isinstance(i, Location)]
    if not here:
        try:
            spots.remove(narrator.get_state(Spot))
        except ValueError:
            pass

    notes = "\n".join(
        "<li><p>{0.html}</p></li>".format(i)
        for i in getattr(narrator, "memories", [])
    )
    items = "\n".join(
        "<li>{0.label}</li>".format(i) for i in ensemble
        if not isinstance(i, (Location, Persona)) and hasattr(i, "label")
    )
    moves = "\n".join(
        "<li>{0}</li>".format(location_to_html(i, path="/{0.id.hex}/".format(narrator)))
        for i in ensemble
        if isinstance(i, Location) and i.get_state(Spot) in spots
    )
    return f"""
<section class="fit-banner">
<h1><span>Blue</span><span>Monday</span><span>78</span></h1>
<h2>{narrator.clock.strftime("%H:%M:%S %p")}</h2>
<h2>{narrator.clock.strftime("%a %d %b")}</h2>
</section>
<div class="fit-speech">
<main>
<ul class="obj-memory">
{notes}
</ul>
<ul class="obj-inventory">
{items}
</ul>
</main>
<nav>
<ul class="obj-move">
{moves}
</ul>
</nav>
</div>"""


def frame_to_html(frame, ensemble=[], title="", final=False):
    heading = " ".join("<span>{0}</span>".format(i.capitalize()) for i in title.split(" "))
    narrator = ensemble[-1] if ensemble else None
    ts = narrator and MultiMatcher.parse_timespan(str(narrator.state))[0]
    spot = narrator.get_state(Spot) if narrator else None
    dialogue = "\n".join(animated_line_to_html(i) for i in frame[Model.Line])
    stills = "\n".join(animated_still_to_html(i) for i in frame[Model.Still])
    audio = "\n".join(animated_audio_to_html(i) for i in frame[Model.Audio])
    return f"""
{audio}
<section class="fit-banner">
<h1>{heading}</h1>
<h2>{ts.strftime("%H:%M:%S %p") if ts else ""}</h2>
<h2>{ts.strftime("%a %d %b") if ts else ""}</h2>
</section>
<aside class="fit-photos">
{stills}
</aside>
<div class="fit-speech">
<main>
{'<h1>{0}</h1>'.format(spot.value[-1].capitalize().replace("_", " ")) if spot is not None else ''}
<ul class="obj-dialogue">
{dialogue}
</ul>
</main>
<nav>
<ul>
<li><form role="form" action="{narrator.id.hex if narrator else ""}/map" method="GET" name="titles">
{'<button action="submit">Go</button>'.format(narrator) if narrator and final else ''}
</form></li>
</ul>
</nav>
</div>"""


def frame_to_text(frame, ensemble=[], title="", final=False):
    return "\n".join(
        ["{0}{1}{2}".format(
            " ".join(filter(None, anim.element.persona.name)) if hasattr(anim.element.persona, "name") else "",
            ": " if hasattr(anim.element.persona, "name") else "",
            anim.element.text
        ) for anim in frame[Model.Line]]
    )


def titles_to_html(config=None, url_pattern=""):
    assembly_widget = f"""
    <label for="input-assembly-url" id="tip-assembly-url">Assembly URL</label>
    <input
    name="assembly_url"
    type="url"
    id="input-assembly-url"
    aria-describedby="tip-assembly-url"
    placeholder="http://"
    pattern="{ url_pattern }"
    title="This server can import JSON data from a URL endpoint. If correctly formatted, that data will be used to
initialise your story."
    >""" if config and config.getboolean("assembly", "enable_user", fallback=False) else ""

    return f"""
<section class="fit-banner">
<h1><span>Blue</span><span>Monday</span><span>78</span></h1>
<h2>A Turberfield episode</h2>
</section>
<div class="fit-speech">
<main>
<h1>Start a new story.</h1>
<p class="obj-speech">You can get the code for this story from
<a href="https://github.com/tundish/blue_monday_78">GitHub</a>.</p>
</main>
<nav>
<ul>
<li><form role="form" action="/" method="POST" name="titles" class="grid-flash mod-titles">
    <fieldset>
    { assembly_widget }
    <button type="submit">Go</button>
    </fieldset>
</form></li>
</ul>
</nav>
</div>"""


def feed_to_html(pages, root, config=None, url_pattern=""):
    assembly_widget = f"""
    <label for="input-assembly-url" id="tip-assembly-url">Assembly URL</label>
    <input
    name="assembly_url"
    type="url"
    id="input-assembly-url"
    aria-describedby="tip-assembly-url"
    placeholder="http://"
    pattern="{ url_pattern }"
    title="This server can import JSON data from a URL endpoint. If correctly formatted, that data will be used to
initialise your story."
    >""" if config and config.getboolean("assembly", "enable_user", fallback=False) else ""
    feed_list = "\n".join(
        '<li><a href="{0}">{1}</a></li>'.format(page.path.relative_to(root).as_posix(), page.title.title())
        for page in pages
        if not page.ordinal
    )


    return f"""
<section class="fit-banner">
<h1><span>Blue</span><span>Monday</span><span>78</span></h1>
<h2>A Turberfield episode</h2>
</section>
<div class="fit-speech">
<main>
<h1>Contents</h1>
<ul>
{ feed_list }
</ul>
</main>
<nav>
<ul>
</ul>
</nav>
</div>"""


def dict_to_css(mapping=None, tag=":root"):
    mapping = mapping or {}
    entries = "\n".join("--{0}: {1};".format(k, v) for k, v in mapping.items())
    return f"""{tag} {{
{entries}
}}"""


@functools.lru_cache()
def body_html(title="", refresh=None, next_=""):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{'<meta http-equiv="refresh" content="{0};/{1}">'.format(refresh, next_) if refresh and next_ else ''}
<meta http-equiv="X-UA-Compatible" content="ie=edge">
<title>{title}</title>
<link rel="stylesheet" href="/css/bfost.css" />
</head>
<body>
<style type="text/css">
{{0}}
</style>
{{1}}
</body>
</html>"""


