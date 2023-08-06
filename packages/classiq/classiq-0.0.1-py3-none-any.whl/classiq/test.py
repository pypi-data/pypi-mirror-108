import asyncio

from classiq import generator, client

client.client.refresh_access_token()
gen = generator.Generator(max_depth=1, qubit_count=1)
asyncio.run(gen.generate())
