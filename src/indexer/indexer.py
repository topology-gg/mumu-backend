from apibara import EventFilter, IndexerRunner, Info, NewEvents
from apibara.indexer import IndexerRunnerConfiguration
from starknet_py.contract import FunctionCallSerializer, identifier_manager_from_abi
from .abis import mech_state_abi, grid_abi, new_simulation_abi, end_summary_abi
from .types import NewSimulation, EndSummary

indexer_id = "mumu-indexer"

new_simulation_decoder = FunctionCallSerializer(
    abi=new_simulation_abi,
    identifier_manager=identifier_manager_from_abi([mech_state_abi, grid_abi, new_simulation_abi]),
)

end_summary_decoder = FunctionCallSerializer(
    abi=end_summary_abi,
    identifier_manager=identifier_manager_from_abi([end_summary_abi]),
)

def decode(event_ns, event_es):
    ns = NewSimulation.from_iter(iter(event_ns.data))
    es = EndSummary.from_iter(iter(event_es.data))
    return dict(
        solver = ns.solver,
        mechs = [m.to_json() for m in ns.mechs],
        instructions_sets = ns.instructions_sets,
        instructions = ns.instructions,
        operators_inputs = [i.to_json() for i in ns.operators_inputs],
        operators_outputs = [i.to_json() for i in ns.operators_outputs],
        operators_type = ns.operators_type,
        static_cost = ns.static_cost,
        delivered = es.delivered,
        latency = es.latency,
        dynamic_cost = es.dynamic_cost,
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
                address="0x06fea4edba44e89743f728a0c03bed6bf3cfeb99a43aa6d57c64dffc4d0a2538",
            ),
            EventFilter.from_event_name(
                name="end_summary",
                address="0x06fea4edba44e89743f728a0c03bed6bf3cfeb99a43aa6d57c64dffc4d0a2538",
            )
        ],
        index_from_block=396_137,
    )

    print("Initialization completed. Entering main loop.")

    await runner.run()
