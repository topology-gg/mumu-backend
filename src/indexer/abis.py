end_summary_abi = {
    "name": "end_summary",
    "type": "event",
    "keys": [],
    "outputs": [
        {"name": "delivered", "type": "felt"},
        {"name": "latency", "type": "felt"},
        {"name": "dynamic_cost", "type": "felt"}
    ], }

mech_state_abi = {
    "name": "MechState",
    "type": "struct",
    "size": 5,
    "members": [
            {"name": "id", "offset": 0, "type": "felt"},
            {"name": "type", "offset": 1, "type": "felt"},
            {"name": "status", "offset": 1, "type": "felt"},
            {"name": "index", "offset": 1, "type": "Grid"},
    ],
}

grid_abi = {
    "name": "Grid",
    "type": "struct",
    "size": 2,
    "members": [
            {"name": "x", "offset": 0, "type": "felt"},
            {"name": "y", "offset": 1, "type": "felt"},
    ],
}

new_simulation_abi = {
    "name": "new_simulation",
    "type": "event",
    "keys": [],
    "outputs": [
            {"name": "solver", "type": "felt"},
            {"name": "mechs_len", "type": "felt"},
            {"name": "mechs", "type": "MechState*"},
            {"name": "instructions_sets_len", "type": "felt"},
            {"name": "instructions_sets", "type": "felt*"},
            {"name": "instructions_len", "type": "felt"},
            {"name": "instructions", "type": "felt*"},
            {"name": "operators_inputs_len", "type": "felt"},
            {"name": "operators_inputs", "type": "Grid*"},
            {"name": "operators_outputs_len", "type": "felt"},
            {"name": "operators_outputs", "type": "Grid*"},
            {"name": "operators_type_len", "type": "felt"},
            {"name": "operators_type", "type": "felt*"},
            {"name": "static_cost", "type": "felt"},
    ],
}
