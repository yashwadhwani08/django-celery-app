import base64
import os
from time import sleep
import copy

from celery import shared_task
from django.conf import settings
import requests
from .models import PromptToImage
from django.core.files.base import ContentFile


URL = "https://api.waifu.im/search"
API_HOST = os.getenv("API_HOST", "https://api.stability.ai")
API_KEY = settings.API_KEY
ENGINE_ID = "stable-diffusion-xl-1024-v1-0"


@shared_task()
def send_request_to_server(prompt, row_id):
    print(API_KEY)
    print(API_HOST)
    print(type(prompt), type(row_id))
    print(f"{prompt} received with id {row_id}")

    if API_KEY is None:
        raise Exception("Missing Stability API key.")

    response = requests.post(
        f"{API_HOST}/v1/generation/{ENGINE_ID}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
        json={
            "text_prompts": [{"text": prompt}],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        },
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    metadata = copy.deepcopy(data)

    for img_data in metadata["artifacts"]:
        del img_data["base64"]

    print(metadata)

    promptToImageObject = PromptToImage.objects.get(id=row_id)
    promptToImageObject.meta_data = metadata
    for image in data["artifacts"]:
        img = base64.b64decode(image["base64"])
        promptToImageObject.image_output.save(
            f"{prompt.strip()}.png", ContentFile(img), save=True
        )
