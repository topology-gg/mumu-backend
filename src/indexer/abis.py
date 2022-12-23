end_summary_abi = {
    "name": "end_summary",
    "type": "event",
    "keys": [],
    "outputs": [
        {"name": "delivered", "type": "felt"},
        {"name": "latency", "type": "felt"},
        {"name": "dynamic_cost", "type": "felt"},
    ],
}

atom_faucet_state_abi = {
    "name": "AtomFaucetState",
    "type": "struct",
    "size": 4,
    "members": [
        {"name": "id", "offset": 0, "type": "felt"},
        {"name": "type", "offset": 1, "type": "felt"},
        {"name": "index", "offset": 2, "type": "Grid"},
    ],
}

atom_sink_state_abi = {
    "name": "AtomFaucetState",
    "type": "struct",
    "size": 3,
    "members": [
        {"name": "id", "offset": 0, "type": "felt"},
        {"name": "index", "offset": 1, "type": "Grid"},
    ],
}

mech_state_abi = {
    "name": "InputMechState",
    "type": "struct",
    "size": 6,
    "members": [
        {"name": "id", "offset": 0, "type": "felt"},
        {"name": "type", "offset": 1, "type": "felt"},
        {"name": "status", "offset": 2, "type": "felt"},
        {"name": "index", "offset": 3, "type": "Grid"},
        {"name": "description", "offset": 5, "type": "felt"},
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
        {"name": "music_title", "type": "felt"},
        {"name": "mechs_len", "type": "felt"},
        {"name": "mechs", "type": "InputMechState*"},
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
        {"name": "mech_volumes_len", "type": "felt"},
        {"name": "mech_volumes", "type": "felt*"},
        {"name": "faucets_len", "type": "felt"},
        {"name": "faucets", "type": "AtomFaucetState*"},
        {"name": "sinks_len", "type": "felt"},
        {"name": "sinks", "type": "AtomSinkState*"},
        {"name": "static_cost", "type": "felt"},
    ],
}
