#!/usr/local/bin/python3
import click
import yaml


def _tag(value, *tags):
    if len(tags):
        return f"<{tags[-1]}>" + _tag(value, *(tags[:-1])) + f"</{tags[-1]}>"
    return value


def _split_name(value, padding_size=3):
    has_strike = "strike" in value
    padding = ["" for a in range(padding_size)]
    out = ""
    for i, v in enumerate((value["name"].split(" - ") + padding)[:padding_size]):
        if i in [1, 2]:
            v = _tag(v, "kbd")
        if has_strike:
            out += _tag(v, "strike", "td")
        else:
            out += _tag(v, "td")
    return out


def _dict(values):
    return _tag("".join(_tag(f"{k}: {values[k]}", "li") for k in values), "ul")


def _link(value):
    return f'<a target="_blank" rel="noopener noreferrer" href="{value}">{value}</a>'


def _helper(value):
    if isinstance(value, dict):
        if len(value) > 1 and set(value.keys()) != {"name", "strike"}:
            out = ""
            for k in value:
                if k in ["name", "strike"]:
                    continue
                if "http" in str(value[k]):
                    out += _tag(_link(value[k]), "li")
                elif isinstance(value[k], dict):
                    out += _tag(f"{k}:", "li") + _dict(value[k])
                else:
                    out += _tag(f"{k}: {value[k]}", "li")
            return _tag(_split_name(value) + _tag(out, "ul", "details", "td"), "tr")
        else:
            return _tag(_split_name(value, 4), "tr")
    return _tag(value, "td", "tr")


@click.command()
@click.argument("src")
def main(src):
    with open(src) as f:
        # https://www.tutorialspoint.com/yaml/index.htm
        data = yaml.load(f, yaml.FullLoader)
    for key in data:
        print(_tag(key, "h2"))
        print("<table>")
        for value in data.get(key):
            print(_helper(value))
        print("</table>")
    print(
        """<style>
strike {
    color: #999;
}
table {
    border-collapse: collapse;
    border-spacing: 0;
}
tbody tr:nth-child(odd) {
    background: #eee;
}
td {
    padding: 3px 10px 3px 15px;
}
ul {
    margin: 1px;
}
</style>
"""
    )


if __name__ == "__main__":
    main()
