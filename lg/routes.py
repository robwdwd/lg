# Copyright (c) 2023, Rob Woodward. All rights reserved.
#
# This file is part of Looking Glass Tool and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Setup routes."""

from starlette.routing import Route

from lg.home import home
from lg.ping_multi import ping_multi


routes = [
    Route("/", endpoint=home, name="home", methods=["GET", "POST"]),
    Route("/pingmulti", endpoint=ping_multi, name="ping_multi", methods=["GET", "POST"]),
]
