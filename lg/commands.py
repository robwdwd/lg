# Copyright (c) 2023, Rob Woodward. All rights reserved.
#
# This file is part of Looking Glass Tool and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""CLI command parser."""

from lg import settings


def get_ping_multi_cmds(locations: list, ip_addresses: list) -> dict:
    """Get commands and devices types to run based on location and ip addresses.

    Args:
        locations (list): List of locations to run ping from
        ip_addresses (list): List of IP addresses to run ping to

    Returns:
        dict: Devices and commands table
    """
    results = {}

    for location in locations:
        cli_cmds = []
        device = settings.CONFIG_FILE["locations"][location]["device"]
        device_type = settings.CONFIG_FILE["locations"][location]["type"]
        source = settings.CONFIG_FILE["locations"][location]["source"]
        location_name = settings.CONFIG_FILE["locations"][location]["name"]

        for ip_address in ip_addresses:
            cli_cmd = settings.CONFIG_FILE["commands"]["ping"][device_type].replace("IPADDRESS", ip_address)
            cli_cmd = cli_cmd.replace("SOURCE", source)

            cli_cmds.append(cli_cmd)

            results[device] = {"location_name": location_name, "type": device_type, "cmds": cli_cmds}

    return results


def get_cmd(location: str, command: str, ip_address: str):
    """Get command to run on devices after user submits looking glass form.

    Args:
        location (str): Location user selected
        command (str): Command user selected (bgp, ping, traceroute)
        ip (str): IP or CIDR user entered

    Returns:
        dict: Device, type of device and cli commands to run
    """
    device = settings.CONFIG_FILE["locations"][location]["device"]
    device_type = settings.CONFIG_FILE["locations"][location]["type"]
    source = settings.CONFIG_FILE["locations"][location]["source"]

    cli_cmd = settings.CONFIG_FILE["commands"][command][device_type].replace("IPADDRESS", ip_address)
    if command != "bgp":
        cli_cmd = cli_cmd.replace("SOURCE", source)

    return {"device": device, "type": device_type, "cmd": cli_cmd}
