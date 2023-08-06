import uuid

from classiq import client
from classiq_interface.generator import constraints, result


class ApiWrapper:
    def __init__(self):
        # TODO: allow determining the configuration manually
        self._client = client.client

    async def start_generation_task(
        self, constraints_obj: constraints.QuantumCircuitConstraints
    ) -> uuid.UUID:
        task_id = await self._client.call_api(
            http_method="post",
            url="/api/v1/tasks/generate",
            body=constraints_obj.dict(exclude_defaults=True),
        )

        if not isinstance(task_id, str):
            raise Exception(f"Unexpected returned value: {task_id}")

        return uuid.UUID(task_id)

    async def get_generation_result(
        self, task_id: uuid.UUID
    ) -> result.GenerationResult:
        data = await self._client.call_api(
            http_method="get", url=f"/api/v1/tasks/{task_id}"
        )

        if not isinstance(data, dict):
            raise Exception(f"Unexpected returned value: {data}")

        return result.GenerationResult.parse_obj(data)
