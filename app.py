# Copyright (c) 2023, Rob Woodward. All rights reserved.
#
# This file is part of Looking Glass Tool and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Helper App to run ip web tools in development mode."""
import uvicorn
from lg import settings

if __name__ == "__main__":
    uvicorn.run(
        "lg:app",
        host=settings.LISTEN,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL,
        reload=settings.DEBUG,
        root_path=settings.ROOT_PATH
    )
