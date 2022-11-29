import json
from pydantic import BaseModel
import vonage
import logging
import os
from app.common import Result


log = logging.getLogger('default')


class VoiceCall(BaseModel):
    phone: str
    msg: str


async def callvonage(phone, msg):
    client = vonage.Client(
        application_id=os.getenv('vonage_application_id'),
        private_key='/etc/app/private.key',
    )

    voice = vonage.Voice(client)

    payload = {
        'to': [{'type': 'phone', 'number': phone}],
        'from': {'type': 'phone', 'number': os.getenv('vonage_number')},
        'ncco': [{'action': 'talk', 'text': msg, 'loop': 2}]
    }
    log.debug("payload is %s" % payload)

    result = Result()
    try:
        voice_response = voice.create_call(payload)
        log.debug(msg="voice response: %s" % json.dumps(voice_response))
        result['code'] = 0
        result['data'] = voice_response
    except Exception as e:
        log.error(e)
        result['error'] = str(e)
    return result
