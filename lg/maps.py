# Copyright (c) 2023, Rob Woodward. All rights reserved.
#
# This file is part of Filter Gen and is released under the
# "BSD 2-Clause License". Please see the LICENSE file that should
# have been included as part of this distribution.
#
"""Map communities and ASNs to more human values."""


import sqlite3
import re


def init_db():
    """Initialise the mappings database."""
    db_con = sqlite3.connect("mapsdb/maps.db")

    db_cursor = db_con.cursor()
    db_cursor.execute("DROP TABLE IF EXISTS communities")
    db_cursor.execute("CREATE TABLE communities(community, name)")

    records = []

    with open("mapsdb/communities.txt", "r") as communities_file:
        for line in communities_file:
            line = line.strip()
            if line.startswith("#") or not line:
                continue

            data = re.split(r"\s+", line, maxsplit=1)
            if len(data) == 2:
                records.append(data)

    db_cursor.executemany("INSERT INTO communities VALUES(?,?);", records)
    db_con.commit()
    db_con.close()


def process_bgp_output(output: dict) -> dict:
    """Process the output of the BGP command.

    Args:
        output (dict): Device Output

    Returns:
        dict: Processed dvice output
    """
    db_con = sqlite3.connect("mapsdb/maps.db")
    db_cursor = db_con.cursor()

    for prefix in output:
        for path in output[prefix]["paths"]:
            communities = path["communities"]

            if communities:
                sql = "SELECT * FROM communities WHERE community IN ('" + "','".join(communities) + "')"
                res = db_cursor.execute(sql)

                com_map = dict(res.fetchall())
                new_comms = []
                for community in communities:
                    if community in com_map:
                        new_comms.append({"community": community, "map": com_map[community]})
                    else:
                        new_comms.append({"community": community, "map": None})

                path["communities"] = new_comms

    db_con.close()

    return output
