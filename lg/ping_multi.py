# Copyright (c) 2023, Rob Woodward. All rights reserved.
#
# This file is part of Looking Glass Tool and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Multi-Ping Page."""

import asyncio
from starlette_wtf import csrf_protect

from lg.forms import PingMultiForm
from lg.templates import templates
from lg.runcmd import get_output
from lg.commands import get_ping_multi_cmds
from lg.ttp import get_template, parse_txt


async def run_device(hostname: str, device: dict, raw_output: bool):
    location_name = device["location_name"]
    try:
        response = await get_output(
            hostname=hostname,
            device_type=device["type"],
            cli_cmds=device["cmds"],
            timeout=60,
        )
        print(response.result)
        device_output = "\n".join(resp.result for resp in response.data)

        if not raw_output:
            device_output = parse_txt(device_output, device["template"])[0]

        print(device_output)

    except Exception as err:
        raise Exception(f"ERROR: Getting output failed for {location_name}: {err}")

    return {"output": device_output, "location": location_name}


async def process_lg_fields(form):
    """Process fields on the lg form.

    Args:
        form (Form): WTForm being proccessed

    Returns:
        dict: Device output
    """
    locations = list(form.locations.data)
    ipaddresses = str(form.ipaddresses.data)
    raw_output = bool(form.raw_output.data)

    ipaddresses = ipaddresses.split()

    # Remove duplicates
    ipaddresses = list(dict.fromkeys(ipaddresses))

    devices = get_ping_multi_cmds(locations, ipaddresses)

    output_table = {"devices": {}, "errors": [], "raw_output": raw_output}

    for hostname, device in devices.items():
        template_name = get_template("ping", device["type"])
        device["template"] = template_name

        # If any device is missing a template revert back to raw output
        # for all devices.
        if not template_name:
            output_table["raw_output"] = True
            raw_output = True

    # Gather output from each device.
    #
    responses = []
    try:
        tasks = [run_device(hostname, device, raw_output) for hostname, device in devices.items()]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

    except Exception as err:
        output_table["errors"].append(str(err))

    for response in responses:
        if isinstance(response, Exception):
            print(response)
            output_table["errors"].append(str(response))
        else:
            print(response)
            location_name = response["location"]
            output_table["devices"][location_name] = response["output"]

    return output_table


@csrf_protect
async def ping_multi(request):
    """LG multiple destination ping page entry point."""
    results = None

    form = await PingMultiForm.from_formdata(request)

    if await form.validate_on_submit():
        results = await process_lg_fields(form)

    return templates.TemplateResponse("ping_multi.html", {"request": request, "results": results, "form": form})
