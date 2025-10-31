import asyncio
import aio_pika
from app.config import settings


async def connect_rabbitmq():
    """Establish a connection to RabbitMQ server."""
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    channel = await connection.channel()
    await channel.declare_exchange("chat_exchange", aio_pika.ExchangeType.TOPIC)
    print("✅ Connected to RabbitMQ and exchange declared")
    return connection, channel
