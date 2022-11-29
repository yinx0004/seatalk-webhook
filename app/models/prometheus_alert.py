from typing import Dict, List
from pydantic import BaseModel, Field
from app.common import convert_sgt, get_contact, Result
from app.models.seatalk_bot import callseatalk
from app.models.voicecall import callvonage
from app.lib.duty_schedule import get_agent
import logging


log = logging.getLogger('default')


class Alert(BaseModel):
    fingerprint: str = None
    status: str = None
    starts_at: str = Field(alias="startsAt")
    ends_at: str = Field(alias="endsAt")
    generator_url: str = Field(alias="generatorURL")
    silence_url: str = Field(alias="silenceURL")
    annotations: Dict[str, str] = None
    labels: Dict[str, str] = None
    value_string: str = Field(alias="valueString")

    class Config:
        extra = "allow"
        allow_population_by_field_name = True


class AlertGroup(BaseModel):
    receiver: str = None
    status: str = None
    external_url: str = Field(alias="externalURL")
    version: str = None
    group_key: str = Field(alias="groupKey")
    truncated_alerts: int = Field(alias="truncatedAlerts")
    group_labels: Dict[str, str] = Field(alias="groupLabels")
    common_annotations: Dict[str, str] = Field(alias="commonAnnotations")
    common_labels: Dict[str, str] = Field(alias="commonLabels")
    alerts: List[Alert] = None

    class Config:
        extra = "allow"
        allow_population_by_field_name = True


def format_alert(alert_group):
    log.debug("send_alert")
    content = ""
    try:
        for alert in alert_group.alerts:
            print(alert)
            alert_status = alert.status
            alert_annotations = alert.annotations
            starts_at = convert_sgt(alert.starts_at)
            ends_at = convert_sgt(alert.ends_at)
            generator_url = alert.generator_url
            # silence_url = alert.silence_url
            if alert.status == "resolved":
                alert_str = "__Status__: %s\n\n__Annotations__: %s\n\n__Starts__: %s\n\n__Ends__: %s\n\n" \
                % (alert_status, alert_annotations, starts_at, ends_at)
            else:
                alert_str = "__Status__: %s\n\n__Annotations__: %s\n\n__Starts__: %s\n\n__Generator__: %s\n\n"\
                            % (alert_status, alert_annotations, starts_at, generator_url)
            content += alert_str
        log.debug("content: %s" % content)
    except Exception as e:
        log.error(e)

    return content


async def send_seatalk_alert(token, alert_group):
    msg = format_alert(alert_group)
    log.debug("alert: %s" % msg)
    result = await callseatalk(token, msg)
    return result


async def send_voice_alert(token, alert_group):
    result = Result(code=0, message="Success")
    msg = format_alert(alert_group)
    msg = "Voice call sent to you.\n\n" + msg
    log.debug("alert: %s" % msg)
    agent = get_agent()
    log.debug("agent: %s" % agent)
    phone, email = get_contact(agent)
    log.debug("phone: %s, email: %s " % (phone, email))
    voice_result = await callvonage(phone, msg)
    if voice_result['code'] != 0:
        return voice_result
    seatalk_result = await callseatalk(token, msg, email)
    if seatalk_result['code'] != 0:
        return seatalk_result
    return result
