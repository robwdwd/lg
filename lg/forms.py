# Copyright (c) 2023, Rob Woodward. All rights reserved.
#
# This file is part of Looking Glass Tool and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Application forms."""
import ipaddress
from starlette_wtf import StarletteForm
from wtforms import SelectField, StringField, ValidationError, BooleanField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired
from lg import settings


def get_locations():
    """Get a list of locations from config file for Location select form field.

    Returns:
        list: List of location index, location name tuples.
    """
    choices = {}

    for location, data in settings.CONFIG_FILE["locations"].items():
        if data["region"] not in choices:
            choices[data["region"]] = []
        choices[data["region"]].append((location, data["name"]))

    return choices


class PingMultiForm(StarletteForm):
    """Form for Multi-Ping Page."""

    locations = SelectMultipleField("Location", choices=get_locations(), validators=[DataRequired()])
    ipaddresses = TextAreaField("IP Addresses", validators=[DataRequired()])
    raw_output = BooleanField("Plain text output")

    def validate_ipaddresses(form, field):
        """Validate the IP address or CIDR

        Args:
            form (StarletteForm): Current Form
            field (StringField): IP address field

        Raises:
            ValidationError: When not a valid IP Address or CIDR.
        """

        # Check IP address is valid.
        #
        ipaddresses = field.data.split()
        if len(ipaddresses) > settings.PING_MULTI_MAX_IP:
            raise ValidationError(f"Maximum of {settings.PING_MULTI_MAX_IP} IP addresses allowed.")

        try:
            for ipaddr in ipaddresses:
                ipaddress.ip_address(ipaddr)
        except ValueError as exc:
            raise ValidationError(str(exc))

    def validate_locations(form, field):
        """Validate locations

        Args:
            form (StarletteForm): Current Form
            field (StringField): Location field

        Raises:
            ValidationError: When number of locations is greater than three
        """

        if len(field.data) > settings.PING_MULTI_MAX_SOURCE:
            raise ValidationError(f"A maximum of {settings.PING_MULTI_MAX_SOURCE} locations are allowed.")


class HomeForm(StarletteForm):
    """Form for Home Page."""

    location = SelectField("Location", choices=get_locations(), validators=[DataRequired()])
    command = SelectField(
        "Command",
        choices=[("ping", "Ping"), ("traceroute", "Traceroute"), ("bgp", "BGP Route")],
        validators=[DataRequired()],
    )
    ipaddress = StringField("IP Address or CIDR", validators=[DataRequired()])
    raw_output = BooleanField("Plain text output")

    def validate_ipaddress(form, field):
        """Validate the IP address or CIDR

        Args:
            form (StarletteForm): Current Form
            field (StringField): IP address field

        Raises:
            ValidationError: When not a valid IP Address or CIDR.
        """

        # Check IP address is valid.
        #
        try:
            if "/" in field.data:
                ipaddress.ip_network(field.data)
            else:
                ipaddress.ip_address(field.data)
        except ValueError as exc:
            raise ValidationError(str(exc))

        # Check that CIDR notation is not used for ping and traceroute commands
        #
        if form.command.data != "bgp" and "/" in field.data:
            raise ValidationError("Cidr notation not valid for ping or traceroute.")
