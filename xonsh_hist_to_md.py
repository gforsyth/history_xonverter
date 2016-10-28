import re
import sys
import json
import jinja2

# regex to remove escape sequences (markdown no like)
ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')

# simple input/output template in markdown
md_in_out = jinja2.Template('''
```console
{{ prompt }}{{ inp|indent(len(prompt) + 4)}}
```

{% if outp.strip() %}
```console
{{ outp }}```
{% endif %}
''')

# load xonsh history


def render_io(history, file='test.md'):
    """Loop over history file, printing input and output if output is stored,
    otherwise print nothing
    """
    with open(file, 'a') as f:
        for entry in [i for i in history['data']['cmds'] if 'out' in i]:
            inp = ansi_escape.sub('', entry['inp'])
            out = ansi_escape.sub('', entry['out'])
            mdout = md_in_out.render(inp=inp, outp=out)
            f.write(mdout)

if __name__ == '__main__':
    with open(sys.argv[1], 'r') as f:
        a = json.load(f)
    render_io(a)
