from uuid import uuid4
import boto3
import botocore.exceptions


class NotificationManager:

    def __init__(self, resource_name: str):
        sns = boto3.resource("sns")
        self._sns_topic = sns.Topic(resource_name)

    def publish(self, event_type: str, message, group_id: str):
        if type(message) is not str:
            message = message.json()
        try:
            response = self._sns_topic.publish(
                Message=message,
                MessageDeduplicationId=uuid4().hex,
                MessageGroupId=group_id,
                MessageAttributes={"eventType": event_type},
            )
        except botocore.exceptions.ClientError as e:
            raise InternalError() from e


class NotificationManagerMock:

    def __init__(self, resource_name: str):
        pass

    def publish(self, event_type: str, message, group_id: str):
        pass


class InternalError(Exception):
    pass
