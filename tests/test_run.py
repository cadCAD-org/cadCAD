from cadCAD_diagram.config_diagram import diagram


def policy_1(p, s, h, v):
    return {"pi_1": v["var_1"]}


def policy_2(p, s, h, v):
    return {"pi_1": v["var_1"], "pi_2": v["var_1"] * v["var_2"]}


def suf_1(p, s, h, v, pi):
    return ("var_1", pi["pi_1"])


def suf_2(p, s, h, v, pi):
    return ("var_2", pi["pi_2"])


psubs = [
    {
        "label": "Test",
        "policies": {"policy_1": policy_1, "policy_2": policy_2},
        "variables": {"var_1": suf_1, "var_2": suf_2},
    }
]

initial_state = {"var_1": 0, "var_2": 1}

params = {"param_1": 0, "param_2": 1}


def test_run():
    return diagram(initial_state, params, psubs)
