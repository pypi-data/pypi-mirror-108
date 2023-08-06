import functools
from enum import Enum
from typing import Optional, Dict

from classiq import api_wrapper, wire
from classiq_interface.generator import (
    constraints,
    result,
    segments,
    function_param_list,
    function_params,
)


class Generator:
    def __init__(self, qubit_count: int, max_depth: int, **kwargs):
        self._constraints = constraints.QuantumCircuitConstraints(
            qubits_count=qubit_count, max_depth=max_depth, **kwargs
        )

    async def generate(self) -> result.GeneratedCircuit:
        wrapper = api_wrapper.ApiWrapper()
        task_id = await wrapper.start_generation_task(self._constraints)
        generation_result = await wrapper.get_generation_result(task_id)

        if generation_result.status != result.GenerationStatus.SUCCESS:
            raise Exception(f"Generation failed: {generation_result.details}")

        return generation_result.details

    @property
    def constraints(self):
        return self._constraints

    def _add_segment(
        self,
        function: str,
        params: function_params.FunctionParams,
        in_wires: Optional[Dict[Enum, wire.Wire]] = None,
    ) -> Dict[Enum, wire.Wire]:
        if function != type(params).__name__:
            raise Exception("The FunctionParams type does not match function name")

        segment = segments.Segment(function=function, function_params=params)

        if in_wires:
            for in_enum, in_wire in in_wires.items():
                in_wire.connect_wire(end_segment=segment, input_enum=in_enum)

        self._constraints.segments.append(segment)

        return {
            out_enum: wire.Wire(start_segment=segment, output_enum=out_enum)
            for out_enum in params.get_io_enum(function_params.IO.Output)
        }

    def __getattribute__(self, item):
        is_item_function_name = any(
            item == func.__name__
            for func in function_param_list.get_function_param_list()
        )

        if is_item_function_name:
            return functools.partial(self._add_segment, function=item)

        return super().__getattribute__(item)

    def __dir__(self):
        return list(super().__dir__()) + [
            func.__name__ for func in function_param_list.get_function_param_list()
        ]
