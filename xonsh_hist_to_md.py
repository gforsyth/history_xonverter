import re
import json
import jinja2
import argparse

# regex to remove escape sequences (markdown no like)
ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')

# simple input/output template in markdown
md_template = jinja2.Template('''
```console
{{ prompt }} {{ inp|indent(prompt|length + 1)}}
```

{% if outp.strip() %}
```console
{{ outp }}```
{% endif %}
''')

def get_parser():
    parser = argparse.ArgumentParser(description="""Naively render a xonsh
                                    history file into markdown""")
    parser.add_argument('history_json', type=str,
                        help='A xonsh history json file')
    parser.add_argument('output', type=str,
                        help='Markdown file to write/append to')
    parser.add_argument('-p', '--prompt', help='Custom prompt character',
                        default='$')

    return parser

def render_io(history, outfile, prompt):
    """Loop over history file, printing input and output if output is stored,
    otherwise print nothing
    """
    with open(outfile, 'a') as f:
        for entry in [i for i in history['data']['cmds'] if 'out' in i]:
            inp = ansi_escape.sub('', entry['inp'])
            out = ansi_escape.sub('', entry['out'])
            mdout = md_template.render(inp=inp, outp=out, prompt=prompt)
            f.write(mdout)

def main():
    parser = get_parser()
    args = parser.parse_args()

    with open(args.history_json, 'r') as f:
        history = json.load(f)

    render_io(history, args.output, args.prompt)

if __name__ == '__main__':
    main()
