from dataclasses import dataclass
from typing import Iterator, Any

def int64_from_iter(it: Iterator[bytes]):
    return int.from_bytes(next(it), "big")

@dataclass
class Grid: 
    x:int
    y: int

    @staticmethod
    def from_iter(it: Iterator[bytes]):
        x = int64_from_iter(it)
        y = int64_from_iter(it)
        return Grid(x, y)
    def to_json(self) -> Any:
        return {"x": self.x, "y": self.y}

@dataclass
class MechState:
    id: int
    type: int
    status: int
    index: Grid

    @staticmethod
    def from_iter(it: Iterator[bytes]):
        id = int64_from_iter(it)
        type = int64_from_iter(it)
        status = int64_from_iter(it)
        index = Grid.from_iter(it)
        return MechState(id, type, status, index)
    def to_json(self) -> Any:
        return {"id": self.id, "type": self.type, "status": self.status, "index": self.index.to_json()}

@dataclass
class NewSimulation:
        solver: str
        mechs: list[MechState]
        instructions_sets: list[int]
        instructions: list[int]
        operators_inputs: list[int]
        operators_outputs: list[int]
        operators_type: list[int]
        static_cost: int

        @staticmethod
        def from_iter(it: Iterator[bytes]):
            solver = str(int.from_bytes(next(it), "big"))
            mechs_len = int64_from_iter(it)
            mechs = [MechState.from_iter(it) for _ in range(mechs_len)]
            instructions_sets_len = int64_from_iter(it)
            instructions_sets = [int64_from_iter(it) for _ in range(instructions_sets_len)]
            instructions_len = int64_from_iter(it)
            instructions = [int64_from_iter(it) for _ in range(instructions_len)]
            operators_inputs_len = int64_from_iter(it)
            operators_inputs = [int64_from_iter(it) for _ in range(operators_inputs_len)]
            operators_outputs_len = int64_from_iter(it)
            operators_outputs = [int64_from_iter(it) for _ in range(operators_outputs_len)]
            operators_type_len = int64_from_iter(it)
            operators_type = [int64_from_iter(it) for _ in range(operators_type_len)]
            static_cost = int64_from_iter(it)
            return NewSimulation(
                solver, 
                mechs, 
                instructions_sets, 
                instructions,
                operators_inputs, 
                operators_outputs,
                operators_type,
                static_cost
            )

@dataclass
class EndSummary:
    delivered: int
    latency: int
    dynamic_cost: int

    @staticmethod
    def from_iter(it: Iterator[bytes]):
        delivered = int64_from_iter(it)
        latency = int64_from_iter(it)
        dynamic_cost = int64_from_iter(it)
        return EndSummary(delivered, latency, dynamic_cost)