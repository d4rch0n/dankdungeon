import os

from jinja2 import Template

TEMPLATE_ROOT = os.path.join(os.path.dirname(__file__), 'templates')
TEMPLATE_PATHS = {
    fn: os.path.join(TEMPLATE_ROOT, fn)
    for fn in os.listdir(TEMPLATE_ROOT)
}
TEMPLATES = {}


def render(fn, **kwargs):
    if fn not in TEMPLATES:
        with open(TEMPLATE_PATHS[fn]) as f:
            data = f.read()
        TEMPLATES[fn] = Template(data)
    return TEMPLATES[fn].render(**kwargs)


def dump(fn, path, **kwargs):
    rendered = render(fn, **kwargs)
    with open(path, 'w') as f:
        f.write(rendered)


def to_filename(name):
    return '_'.join(name.lower().split()).replace('/', '-').replace("'", '')
