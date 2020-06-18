initial_conditions = {
    "box_A": 10,  # as per the description of the example, box_A starts out with 10 marbles in it
    "box_B": 0,  # as per the description of the example, box_B starts out empty
}


def update_A(params, step, sL, s, _input):
    y = "box_A"
    add_to_A = 0
    if s["box_A"] > s["box_B"]:
        add_to_A = -1
    elif s["box_A"] < s["box_B"]:
        add_to_A = 1
    x = s["box_A"] + add_to_A
    return (y, x)


def update_B(params, step, sL, s, _input):
    y = "box_B"
    add_to_B = 0
    if s["box_B"] > s["box_A"]:
        add_to_B = -1
    elif s["box_B"] < s["box_A"]:
        add_to_B = 1
    x = s["box_B"] + add_to_B
    return (y, x)


partial_state_update_blocks = [
    {
        "policies": {},  # We'll ignore policies for now
        "variables": {  # The following state variables will be updated simultaneously
            "box_A": update_A,
            "box_B": update_B,
        },
    }
]

simulation_parameters = {"T": range(10), "N": 1, "M": {}}

from cadCAD.configuration import Configuration

config = Configuration(
    initial_state=initial_conditions,  # dict containing variable names and initial values
    partial_state_update_blocks=partial_state_update_blocks,  # dict containing state update functions
    sim_config=simulation_parameters,  # dict containing simulation parameters
)

from cadCAD.engine import ExecutionMode, ExecutionContext, Executor

exec_mode = ExecutionMode()
exec_context = ExecutionContext(exec_mode.single_proc)
executor = Executor(exec_context, [config])
(
    raw_result,
    tensor,
) = executor.execute()  # The `execute()` method returns a tuple; its first

print(raw_result)
