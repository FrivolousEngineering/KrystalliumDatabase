import asyncio
from pathlib import Path

import starlette

import models
import rfid


def on_card_detected(name: str, card_id: str):
    pass


def on_card_lost(name: str, card_id: str):
    pass


def on_traits_detected(name: str, traits: list[str]):
    pass


def strength_to_purity(strength):
    match strength:
        case 2: return "polluted"
        case 3: return "tarnished"
        case 4: return "dirty"
        case 5: return "blemished"
        case 6: return "impure"
        case 7: return "unblemished"
        case 8: return "lucid"
        case 9: return "stainless"
        case 10: return "pristine"
        case 11: return "immaculate"
        case 12: return "perfect"
        case _: raise RuntimeError(f"Cannot convert strength {strength} to purity")


def error_response(error_code, title, details = ""):
    return starlette.responses.JSONResponse({
        "data": {
            "id": 0,
            "status": error_code,
            "title": title,
            "details": details,
        }
    }, status_code = 500)

async def write_nfc(request):
    json = await request.json()
    data = json.get("data", {})
    sample_type = data["type"]
    attributes = data["attributes"]

    print(data, attributes)

    controller = rfid.RFIDController(on_card_detected, on_card_lost, on_traits_detected,
                                     root_path=Path("/dev/pts"), patterns=["2"])
    devices = controller.list_devices()
    if not devices:
        return error_response(500, "No RFID devices found")

    device = devices[0]

    print("Waiting for device")

    tries = 100
    while not device.ready and tries > 0:
        await asyncio.sleep(0.1)
        tries -= 1

    if not device.ready:
        device.stop()
        return error_response(500, "Device is not ready")

    print("Device ready, waiting for tag")

    tries = 100
    while device.card_id is None and tries > 0:
        await asyncio.sleep(0.1)
        tries -= 1

    if device.card_id is None:
        device.stop()
        return error_response(500, "No RFID tag found")

    command_args = []
    match sample_type:
        case "raw":
            sample = models.RawSample(**attributes)
            device.writeSample("raw", [
                sample.positive_action,
                sample.positive_target,
                sample.negative_action,
                sample.negative_target,
                "depleted" if sample.depleted else "active"
            ])
        case "refined":
            sample = models.RefinedSample(**attributes)
            device.writeSample("refined", [
                sample.primary_action,
                sample.primary_target,
                sample.secondary_action,
                sample.secondary_target,
                strength_to_purity(sample.strength),
            ])
        case "blood":
            # effect = attributes.
            command_args = [
                # attributes.get("")
            ]
        case _:
            device.stop()
            return error_response(400, f"Invalid sample type {sample_type}")

    print("Wait for writing to finish")

    tries = 100
    while device.writing and tries > 0:
        await asyncio.sleep(0.1)
        tries -= 1

    device.stop()

    if tries == 0:
        return error_response(500, "Writing never finished")

    return starlette.responses.Response("", status_code = 204)
