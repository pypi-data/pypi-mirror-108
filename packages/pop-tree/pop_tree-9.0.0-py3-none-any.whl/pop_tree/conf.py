CLI_CONFIG = {
    "output": {
        "source": "rend",
        "default": None,
    },
    "ref": {
        "positional": True,
        "nargs": "?",
    },
    "recurse": {
        "action": "store_true",
    },
    "graph": {},
}

CONFIG = {
    "ref": {
        "type": str,
        "help": "The ref on the hub to show",
        "default": None,
    },
    "graph": {
        "help": "Plugin to use for generating a graph, (I.E. 'simple', 'details', 'json')",
        "default": None,
    },
}

DYNE = {
    "graph": ["graph"],
    "tree": ["tree"],
}
