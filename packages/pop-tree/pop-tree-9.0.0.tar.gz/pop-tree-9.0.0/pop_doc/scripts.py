#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Dict

import pop.hub


def start():
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="tree", omit_class=False)
    hub.pop.config.load(["pop_doc", "pop_tree", "rend"], cli="pop_doc")

    hub.tree.init.load_all()

    tree = hub.tree.init.traverse()
    tree = hub.tree.init.get_ref(tree, hub.OPT.pop_doc.ref)
    ret = hub.tree.init.refs(tree)

    if not (ret or tree):
        raise KeyError(f"Reference does not exist on the hub: {hub.OPT.pop_doc.ref}")

    result = ret[hub.OPT.pop_doc.ref]

    print(hub.output[hub.OPT.rend.output].display(result))
