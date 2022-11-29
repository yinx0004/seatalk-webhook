from fastapi import FastAPI, status
from app.models import voicecall, seatalk_bot, prometheus_alert
from fastapi.responses import Response
import json
import logging.config
from app.lib.log_config import logging_config
from app.common import Result


class CoustomResponse(Response):
    def __init__(self, content, msg, status_code=status.HTTP_424_FAILED_DEPENDENCY, error=None):
        if msg:
            content['msg'] = msg
        if error:
            content['error'] = error
        if content['code'] == 0:
            status_code = status.HTTP_200_OK
        super().__init__(
            content=json.dumps(content),
            media_type="application/json",
            status_code=status_code
        )


logging.config.dictConfig(logging_config)
log = logging.getLogger('default')
app = FastAPI(default_response_class=CoustomResponse)


@app.get("/")
def health():
    result = Result(code=0, data="Healthy")
    return CoustomResponse(content=result, msg="Success", error=None)


@app.post("/seatalk/{token}")
async def send_seatalk(token, seatalk: seatalk_bot.SeaTalk):
    result = await seatalk_bot.callseatalk(token, seatalk.content, seatalk.email)
    return CoustomResponse(content=result, msg=None, error=None)


@app.post("/vonage")
async def send_vonage(voice_call: voicecall.VoiceCall):
    result = await voicecall.callvonage(voice_call.phone, voice_call.msg)
    return CoustomResponse(content=result, msg=None, error=None)


@app.post("/alert/seatalk/{token}")
async def alert_seatalk(token, alert_group: prometheus_alert.AlertGroup):
    log.debug("Alert group: %s" % alert_group)
    result = await prometheus_alert.send_seatalk_alert(token, alert_group)
    return CoustomResponse(content=result, msg=None, error=None)


@app.post("/alert/voice/{token}")
async def alert_voice(token, alert_group: prometheus_alert.AlertGroup):
    log.debug("Alert group: %s" % alert_group)
    result = await prometheus_alert.send_voice_alert(token, alert_group)
    return CoustomResponse(content=result, msg=None, error=None)
