import re
import json
import jinja2

# regex to remove escape sequences (markdown no like)
ansi_escape = re.compile(r'\x1b[^m]*m')

# simple input/output template in markdown
md_in_out = jinja2.Template('''
Input:

```console
{{ inp }}
```

Output:

```console
{{ outp }}
```
''')

# load xonsh history


def render_io(history, file='test.md'):
    """Loop over history file, printing input and output if output is stored,
    otherwise print nothing
    """
    with open(file, 'a') as f:
        for i in history['data']['cmds']:
            if 'out' in i:
                inp = ansi_escape.sub('', i['inp'])
                out = ansi_escape.sub('', i['out'])
                mdout = md_in_out.render(inp=inp, outp=out)
                f.write(mdout)

if __name__ == '__main__':
    with open('history_ex.json', 'r') as f:
        a = json.load(f)
    render_io(a)
