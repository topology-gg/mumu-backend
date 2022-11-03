from apibara import EventFilter, IndexerRunner, Info, NewEvents
from apibara.indexer import IndexerRunnerConfiguration
from starknet_py.contract import FunctionCallSerializer, identifier_manager_from_abi
from .abis import mech_state_abi, grid_abi, new_simulation_abi, end_summary_abi

indexer_id = "mumu-indexer"

new_simulation_decoder = FunctionCallSerializer(
    abi=new_simulation_abi,
    identifier_manager=identifier_manager_from_abi([mech_state_abi, grid_abi, new_simulation_abi]),
)

end_summary_decoder = FunctionCallSerializer(
    abi=end_summary_abi,
    identifier_manager=identifier_manager_from_abi([end_summary_abi]),
)


def decode_new_simulation_event(data):
    data = [int.from_bytes(b, "big") for b in data]
    return new_simulation_decoder.to_python(data)


def decode_end_summary_event(data):
    data = [int.from_bytes(b, "big") for b in data]
    return end_summary_decoder.to_python(data)

def encode_int_as_bytes(n):
    return n.to_bytes(32, "big")

def decode(data_1, data_2):
    ns = decode_new_simulation_event(data_1.data)
    es = decode_end_summary_event(data_2.data)
    return dict(
        solver = encode_int_as_bytes(ns.solver),
        mechs = ns.mechs,
        instructions_sets = ns.instructions_sets,
        instructions = ns.instructions,
        operators_inputs = ns.operators_inputs,
        operators_outputs = ns.operators_outputs,
        operators_type = ns.operators_type,
        static_cost = encode_int_as_bytes(ns.static_cost),
        delivered = encode_int_as_bytes(es.delivered),
        latency = encode_int_as_bytes(es.latency),
        dynamic_cost = encode_int_as_bytes(es.dynamic_cost),
    )


async def handle_events(info: Info, block_events: NewEvents):
    """Handle a group of events grouped by block."""
    print(f"Received events for block {block_events.block.number}")

    new_simulations = block_events.events[0::2]
    end_summaries = block_events.events[1::2]

    events = [
        decode(e1, e2)
        for (e1, e2) in zip(new_simulations, end_summaries)
    ]

    # Insert multiple documents in one call.
    await info.storage.insert_many("events", events)


async def run_indexer(server_url=None, mongo_url=None, restart=None):
    print("Starting Apibara indexer")

    runner = IndexerRunner(
        config=IndexerRunnerConfiguration(
            apibara_url=server_url,
            apibara_ssl=True,
            storage_url=mongo_url,
        ),
        reset_state=restart,
        indexer_id=indexer_id,
        new_events_handler=handle_events,
    )

    # Create the indexer if it doesn't exist on the server,
    # otherwise it will resume indexing from where it left off.
    #
    # For now, this also helps the SDK map between human-readable
    # event names and StarkNet events.
    runner.add_event_filters(
        filters=[
            EventFilter.from_event_name(
                name="new_simulation",
                address="0x04774c58e145332500a2a534fc321968441193b660e2e95c0bab713dbc9b090d",
            ),
            EventFilter.from_event_name(
                name="end_summary",
                address="0x04774c58e145332500a2a534fc321968441193b660e2e95c0bab713dbc9b090d",
            )
        ],
        index_from_block=388_427,
    )

    print("Initialization completed. Entering main loop.")

    await runner.run()
