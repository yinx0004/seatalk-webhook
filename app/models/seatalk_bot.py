import httpx
from pydantic.dataclasses import dataclass
import logging
from app.common import Result


maxMsgLen = 2048
openAPI = "https://openapi.seatalk.io/webhook/group/"
headers = {'content-type': 'application/json'}

log = logging.getLogger('default')


class SeaTalkConfig:
    max_anystr_length = 4096
    validate_assignment = False
    error_msg_templates = {
        'value_error.any_str.max_length': 'max_length:{limit_value}',
    }


@dataclass(config=SeaTalkConfig)
class SeaTalk:
    content: str
    email: str = None


async def callseatalk(token, msg, email=None):
    if len(msg) > maxMsgLen:
        msg = msg[:maxMsgLen]

    url = openAPI + token

    if email is not None:
        msg = "<mention-tag target=\"seatalk://user?email=%s\"/>\n\n%s" % (email, msg)

    payload = {
        "tag": "markdown",
        "markdown": {
            "content": msg
        }
    }

    log.debug("payload: %s" % payload)

    result = Result()
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            response_content = response.json()

            log.info("SeaTalk response status code: %s" % response.status_code)
            log.debug("SeaTalk response content: %s" % response_content['msg'])
            if response.status_code == 200 and response_content['code'] == 0:
                log.info("Sent to seatalk succeed.")
                result['code'] = 0
                result['message'] = "Send to SeaTalk success"
            else:
                log.error("Sent to seatalk failed %s." % response_content)
                result["error"] = response_content
                result['message'] = "Seatalk OpenAPI return error"
    except Exception as e:
        log.error(e)
        result["error"] = str(e)
    return result


