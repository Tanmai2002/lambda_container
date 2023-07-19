# application.py
from typing import Any
import cv2
import json
import os
import boto3
from google.protobuf.json_format import MessageToDict
import mediapipe as mp

from aws_lambda_typing import context as context_, events

mp_pose = mp.solutions.mediapipe.python.solutions.holistic

class Response:
    statusCode: str
    body: Any

    def __init__(self, status: str, data: Any = None, message: str = None) -> None:
        self.status = status
        self.data = data
        self.message = message

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)

    def toLambdaResponse(self):
        return {"statusCode": self.status, "body": {"message": self.message, "data": self.data}}


def handler(event: events.APIGatewayProxyEventV2, context: context_.Context):
    pose = mp_pose.Holistic(
        static_image_mode=True,
        model_complexity=2,
        enable_segmentation=True,
        min_detection_confidence=0.5)

    bucket = event.get('bucket') or os.environ.get('S3_BUCKET_NAME')
    key = event.get('key')

    if bucket is None or key is None:
        return Response(409, message="Bad request").toLambdaResponse()

    local_file_path = f'/tmp/{key}'

    boto3.client('s3').download_file(bucket, key, local_file_path)

    image = cv2.imread(local_file_path)

    # Convert the BGR image to RGB before processing.
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    if not results.pose_landmarks:
        return Response(500, message="Pose not detected").toLambdaResponse()

    return Response(200, {
        "pose_landmarks": MessageToDict(results.pose_landmarks),
        "pose_world_landmarks": MessageToDict(results.pose_world_landmarks),
        "face_landmarks": MessageToDict(results.face_landmarks)
    }).toLambdaResponse()


if __name__ == "__main__":
    print(handler(None, None))