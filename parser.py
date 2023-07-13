import re
import sys
from urllib.parse import unquote
from urllib.parse import parse_qsl


def url_parse(name):
    pattern = re.compile(
        r"""
            (?P<name>[\w\+]+)://
            (?:
                (?P<username>[^:/]*)
                (?::(?P<password>[^@]*))?
            @)?
            (?:
                (?:
                    \[(?P<ipv6host>[^/\?]+)\] |
                    (?P<ipv4host>[^/:\?]+)
                )?
                (?::(?P<port>[^/\?]*))?
            )?
            (?:/(?P<path>[^\?]*))?
            (?:\?(?P<query>.*))?
            """,
        re.X,
    )
    m = pattern.match(name)
    if m is not None:
        components = m.groupdict()
        if components["query"] is not None:
            query = {}
            for key, value in parse_qsl(components["query"]):
                if key in query:
                    query[key] = list(query[key]) if isinstance(query[key], list) else [query[key]]
                    query[key].append(value)
                else:
                    query[key] = value
        else:
            query = None
        components["query"] = query
        if components["username"] is not None:
            components["username"] = unquote(components["username"])
        if components["password"] is not None:
            components["password"] = unquote(components["password"])
        ipv4host = components.pop("ipv4host")
        ipv6host = components.pop("ipv6host")
        components["host"] = ipv4host or ipv6host
        name = components.pop("name")
        if components["port"]:
            components["port"] = int(components["port"])
        return name, components