import asyncio
from app.services.messaging import rabbitmq


async def handle_message(message):
    print("Received:", message.body.decode())


async def run_subscriber(queue_name: str):
    await rabbitmq.connect()
    await rabbitmq.subscribe(queue_name, handle_message)


if __name__ == "__main__":
    asyncio.run(run_subscriber("user_2"))  # Example: listen for user with ID 2
