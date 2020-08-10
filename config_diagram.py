import pandas as pd
import numpy as np
from graphviz import Digraph
import inspect
import ast
import re
from collections import namedtuple


### Inspect functions


def extract_var_key(raw_line: str, var_id: str) -> str:
    """
    Extract the key from an line in the form "dict['key']" or
    "dict.get('key', *args)".
    """
    line = raw_line.strip()[len(var_id) :]
    state_var = ""
    if line[0] == "[":
        state_var = line[2:-2]
    elif line[0:4] == ".get":
        call = line.split("(")[1]
        call = call.split(")")[0]
        call = call.strip()
        sep = "'"
        if call[0] == '"':
            sep = '"'
        state_var = [el for el in call.split(sep) if len(el) > 0][0]
    return state_var


def extract_vars_from_source(source: str, var_id: str) -> set:
    """
    Extract keys from an source code that consumes an dict with
    var_id name.
    """
    regex = (
        r"(("
        + var_id
        + r"\[(\'|\")\w+(\'|\")\])|("
        + var_id
        + r".get\((\'|\")\w+(\'|\")[A-z,\s\"\']*\)))"
    )

    matches = re.findall(regex, source)
    lines = [match[0] for match in matches]
    state_vars = set([extract_var_key(line, var_id) for line in lines])
    return state_vars


def extract_keys(f: callable) -> dict:
    """

    """
    src = inspect.getsource(f)
    params = inspect.signature(f)
    params_key = list(params.parameters)[0]
    state_key = list(params.parameters)[3]
    output = {
        "state": extract_vars_from_source(src, state_key),
        "params": extract_vars_from_source(src, params_key),
    }
    return output


def relate_psub(psub: dict) -> dict:
    """
    Given an dict describing an Partial State Update block, this functions
    generates an dict with three keys: 'params' and 'state' which are sets
    containing all unique parameters and state variables for the PSUB,
    and 'map' for doing an more detailed map.
    """
    psub_relation = {"map": {}, "params": set(), "state": set()}
    unique_params = set()
    unique_vars = set()
    keys = ["policies", "variables"]
    for key in keys:
        type_functions = psub.get(key, {})
        type_keys = {k: extract_keys(v) for k, v in type_functions.items()}
        params_list = [v.get("params", set()) for v in type_keys.values()]
        vars_list = [v.get("state", set()) for v in type_keys.values()]
        if len(params_list) > 0:
            params = set.union(*params_list)
        else:
            params = set()
        if len(vars_list) > 0:
            vars = set.union(*vars_list)
        else:
            vars = set()
        psub_relation["params"] = psub_relation["params"].union(params)
        psub_relation["state"] = psub_relation["state"].union(vars)
        psub_relation["map"][key] = type_keys
    return psub_relation


def generate_relations(psubs) -> list:
    """
    Generates an list of dicts,

    """
    psub_relations = [relate_psub(psub) for psub in psubs]
    return psub_relations


### Diagram functions


def generate_time_graph() -> Digraph:
    time_graph = Digraph("cluster_timestep", engine="dot")
    time_graph.attr(style="filled", bgcolor="pink", dpi="50", rankdir="LR")
    return time_graph


def generate_variables_cluster(variables: dict, i: int, suffix="") -> Digraph:
    state_graph = Digraph("cluster_variables_{}{}".format(i, suffix))
    state_graph.attr(style="filled, dashed", label="State", fillcolor="skyblue")
    for key, value in variables.items():
        name = "variable_{}_{}{}".format(key, i, suffix)
        description = "{} ({})".format(key, type(value).__name__)
        state_graph.node(
            name,
            description,
            shape="cylinder",
            style="filled, solid",
            fillcolor="honeydew",
        ),
    return state_graph


def generate_params_cluster(params: dict, i: int) -> Digraph:
    params_graph = Digraph("cluster_params_{}".format(i))
    params_graph.attr(style="filled, dashed", label="Parameters", fillcolor="skyblue")
    for key, value in params.items():
        name = "param_{}_{}".format(key, i)
        description = "{} ({})".format(key, type(value).__name__)
        params_graph.node(
            name,
            description,
            shape="cylinder",
            style="filled, solid",
            fillcolor="honeydew",
        ),
    return params_graph


def generate_psub_graph(i: int):
    psub_graph = Digraph("cluster_psub_{}".format(i))
    psub_graph.attr(
        style="filled, dashed",
        label=f"Partial State Update Block #{i}",
        fillcolor="thistle",
        center="true",
    )
    return psub_graph


def relate_params(graph: Digraph, params, i, origin=-1) -> Digraph:
    for param in params:
        dst = "param_{}_{}".format(param, i)
        src = "param_{}_{}".format(param, origin)
        graph.edge(src, dst)
    return graph


def generate_policies_cluster(policies: dict, i: int, psub_graph) -> Digraph:
    policy_graph = Digraph("cluster_policy_{}".format(i))
    policy_graph.attr(label="Policies")
    policy_graph.node(
        "agg_{}".format(i),
        "Aggregation",
        shape="circle",
        style="filled,bold",
        fillcolor="greenyellow",
        width="1",
    )
    for key, value in policies.items():
        name = "policy_{}_{}".format(key, i)
        description = "{} ({})".format(key, value.__name__)
        policy_graph.node(
            name,
            description,
            style="filled, bold",
            fillcolor="palegreen",
            shape="cds",
            height="1",
            width="1",
        )
        psub_graph.edge(name, "agg_{}".format(i))
    return psub_graph.subgraph(policy_graph)


def relate(
    graph, relations, i, src_prefix, dst_prefix, suffix="", reverse=False
) -> Digraph:
    for key, value in relations.items():
        dst = "{}_{}_{}".format(dst_prefix, key, i)
        for param in value:
            src = "{}_{}_{}{}".format(src_prefix, param, i, suffix)
            if reverse:
                graph.edge(dst, src)
            else:
                graph.edge(src, dst)
    return graph


def generate_sufs_cluster(sufs: dict, i: int, psub_graph, agg=False) -> Digraph:
    suf_graph = Digraph("cluster_suf_{}".format(i))
    suf_graph.attr(label="State Update Functions")
    for key, value in sufs.items():
        name = "suf_{}_{}".format(key, i)
        description = "{} ({})".format(key, value.__name__)
        suf_graph.node(
            name,
            description,
            style="filled, bold",
            fillcolor="red",
            shape="cds",
            height="1",
            width="1",
        )
        if agg:
            psub_graph.edge("agg_{}".format(i), name)
    return psub_graph.subgraph(suf_graph)


def relate_params_to_sufs(graph, sufs, i) -> Digraph:
    for key, value in sufs.items():
        dst = "suf_{}_{}".format(key, i)
        for param in value:
            src = "param_{}_{}".format(param, i)
            graph.edge(src, dst)
    return graph


def diagram(initial_state, params, psubs):
    """
    Generates an diagram for an cadCAD configuration object.
    """
    relations = generate_relations(psubs)
    time_graph = generate_time_graph()
    for i_psub, psub in enumerate(psubs):
        psub_graph = generate_psub_graph(i_psub)

        # Parameters
        psub_params = relations[i_psub].get("params", set())
        psub_params = {k: params.get(k, None) for k in psub_params}
        psub_vars = relations[i_psub].get("state", set())
        psub_vars = {k: initial_state.get(k, None) for k in psub_vars}
        psub_graph.subgraph(generate_params_cluster(psub_params, i_psub))
        psub_graph.subgraph(generate_variables_cluster(psub_vars, i_psub))
        # psub_graph = relate_params(psub_graph, psub_params, i)

        # Policies
        policies = psub.get("policies", {})
        psub_map = relations[i_psub].get("map", {})
        policy_map = psub_map.get("policies", {})
        policy_inputs = {
            policy: relation["state"] for policy, relation in policy_map.items()
        }
        policy_params = {
            policy: relation["params"] for policy, relation in policy_map.items()
        }
        list_of_inputs = list(policy_inputs.values())
        if len(list_of_inputs) > 0:
            agg = True
            inputs = set.union(*list_of_inputs)
            inputs = {k: initial_state.get(k, None) for k in inputs}
            psub_graph.subgraph(generate_policies_cluster(policies, i_psub, psub_graph))
            psub_graph = relate(psub_graph, policy_params, i_psub, "param", "policy")
            psub_graph = relate(psub_graph, policy_inputs, i_psub, "variable", "policy")
        else:
            agg = False

        # SUFs
        sufs = psub.get("variables", {})
        suf_map = psub_map.get("variables", {})
        sufs_inputs = {
            policy: relation["state"] for policy, relation in suf_map.items()
        }
        sufs_params = {
            policy: relation["params"] for policy, relation in suf_map.items()
        }
        list_of_inputs = list(sufs_inputs.values())
        if len(list_of_inputs) > 0:
            inputs = set.union(*list_of_inputs)
            inputs = {k: initial_state.get(k, None) for k in inputs}
            generate_sufs_cluster(sufs, i_psub, psub_graph, agg=agg)
            psub_graph = relate(psub_graph, sufs_params, i_psub, "param", "suf")
            psub_graph = relate(psub_graph, sufs_inputs, i_psub, "variable", "suf")

            time_graph.subgraph(psub_graph)
    return time_graph


def diagram_from_config(config):
    initial_state = config.initial_state
    params = config.sim_config["M"]
    psubs = config.partial_state_updates
    return diagram(initial_state, params, time_graph, psubs)
