# Copyright (c) 2023, Rob Woodward. All rights reserved.
#
# This file is part of Looking Glass Tool and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Create Jinja2 Templates."""


from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="lg/templates", trim_blocks=True, lstrip_blocks=True)
