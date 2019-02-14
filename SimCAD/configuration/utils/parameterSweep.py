from SimCAD.utils import rename, flatten_tabulated_dict, tabulate_dict


def process_variables(d):
    return flatten_tabulated_dict(tabulate_dict(d))


def config_sim(d):
    if "M" in d:
        return [
            {
                "N": d["N"],
                "T": d["T"],
                "M": M
            }
            for M in process_variables(d["M"])
        ]
    else:
        return d
