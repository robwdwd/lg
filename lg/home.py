# Copyright (c) 2023, Rob Woodward. All rights reserved.
#
# This file is part of Looking Glass Tool and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Home Page."""
# import pprint
from starlette_wtf import csrf_protect

from lg.forms import HomeForm
from lg.templates import templates
from lg.runcmd import get_output
from lg.commands import get_cmd
from lg.maps import process_bgp_output
from lg.ttp import get_template

# pp = pprint.PrettyPrinter(indent=2, width=120)


async def process_lg_fields(form):
    """Process fields on the lg form.

    Args:
        form (Form): WTForm being proccessed

    Returns:
        dict|None: Resulting configuration or None
    """
    location = str(form.location.data)
    command = str(form.command.data)
    ipaddress = str(form.ipaddress.data)
    raw_output = bool(form.raw_output.data)

    cli = get_cmd(location, command, ipaddress)

    timeout = 60

    if command == "traceroute":
        timeout = 360

    try:
        response = await get_output(
            hostname=cli["device"],
            device_type=cli["type"],
            cli_cmds=cli["cmd"],
            timeout=timeout,
        )
    except Exception as err:
        return {"errors": f"Error getting output for {location}: {err}"}

    if not raw_output:
        if template_name := get_template(command, cli["type"]):
            output = response.ttp_parse_output(template=template_name)[0]

            if command == "bgp":
                output = process_bgp_output(output)
        else:
            raw_output = True
            output = response.result
    else:
        output = response.result

    return {"output": output, "raw": raw_output, "command": command}


@csrf_protect
async def home(request):
    """Looking glass page entry point."""
    results = None

    form = await HomeForm.from_formdata(request)

    if await form.validate_on_submit():
        results = await process_lg_fields(form)

    return templates.TemplateResponse("home.html", {"request": request, "results": results, "form": form})
