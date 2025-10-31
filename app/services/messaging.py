import aio_pika
from app.config import settings


class RabbitMQService:
    """
    A simple service class for connecting to RabbitMQ using aio_pika,
    publishing messages, subscribing to queues, and managing connection lifecycle.

    Attributes:
        connection (aio_pika.RobustConnection | None): The active RabbitMQ connection object.
        channel (aio_pika.RobustChannel | None): The active channel for publishing/subscribing messages.
    """

    def __init__(self):
        """
        Initialize the RabbitMQService instance with no connection or channel.
        """
        self.connection = None
        self.channel = None

    async def connect(self):
        """
        Establish a robust connection to RabbitMQ and open a channel.

        Input:
            None

        Output:
            None

        Side effects:
            - Sets self.connection to a live aio_pika connection.
            - Sets self.channel to a channel object for publishing and subscribing.

        Raises:
            aio_pika.exceptions.AMQPConnectionError if connection fails.
        """
        self.connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        self.channel = await self.connection.channel()

    async def publish(self, queue_name: str, message: str):
        """
        Publish a message to a specified queue via the default exchange.

        Args:
            queue_name (str): The name of the queue to publish the message to.
            message (str): The message content to send. Must be UTF-8 encodable.

        Returns:
            None

        Raises:
            RuntimeError if the channel is not connected.
            aio_pika.exceptions.AMQPError if publishing fails.
        """
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()), routing_key=queue_name
        )

    async def subscribe(self, queue_name: str, callback):
        """
        Subscribe to a queue with a callback function for incoming messages.

        Args:
            queue_name (str): The name of the queue to consume messages from.
            callback (Callable[[aio_pika.IncomingMessage], Awaitable]):
                Async function called for each message received. Must accept an IncomingMessage.

        Returns:
            None

        Side effects:
            - Declares the queue if it does not exist.
            - Starts consuming messages in the background.

        Raises:
            RuntimeError if the channel is not connected.
            aio_pika.exceptions.AMQPError if subscribing fails.
        """
        queue = await self.channel.declare_queue(queue_name, durable=True)
        await queue.consume(callback)

    async def disconnect(self):
        """
        Cleanly close the RabbitMQ channel and connection.

        Input:
            None

        Output:
            None

        Side effects:
            - Closes self.channel if it exists and sets it to None.
            - Closes self.connection if it exists and sets it to None.

        Notes:
            Always call this method on shutdown to avoid unclosed connections.
        """
        if self.channel:
            await self.channel.close()
            self.channel = None

        if self.connection:
            await self.connection.close()
            self.connection = None


# Singleton instance for use across the application
rabbitmq = RabbitMQService()
