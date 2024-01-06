import os

from lavoro_library.amqp import RabbitMQProducer
from lavoro_library.model.message_schemas import ItemToMatch, JobPostToMatch, ApplicantProfileToMatch

producer = RabbitMQProducer(os.environ["AMQP_URL"], "item_to_match")
