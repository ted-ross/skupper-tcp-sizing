#!/usr/bin/env python3
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

BUFFER_SIZE = 16384
TIERS       = [(0.5, 8), (0.75, 4), (0.85, 2), (1.0, 2)]

def max_connections(gigabytes, idle_ratio):
    octets               = gigabytes * 1024 * 1024 * 1024
    final_tier_buffers   = None
    last_threshold_ratio = 0.0

    ##
    ## Total the number of idle connections and their consumed memory.
    ##
    total_connections = 0
    total_octets      = 0

    ##
    ## For each tier, calculate the number of idle connections and the memory they consume.
    ##
    for (threshold_ratio, buffers) in TIERS:
        memory_available     = (threshold_ratio - last_threshold_ratio) * octets
        tier_connections     = ((memory_available / (BUFFER_SIZE * buffers)) * idle_ratio)
        final_tier_buffers   = buffers
        last_threshold_ratio = threshold_ratio

        total_connections += tier_connections
        total_octets      += tier_connections * BUFFER_SIZE * buffers

    ##
    ## Assign all remaining memory to non-idle connections in the final tier.
    ## On a fully subscribed router, non-idle connections will abide by the
    ## final tier buffer allocation.
    ##
    remaining_memory = octets - total_octets
    total_connections += remaining_memory / (BUFFER_SIZE * final_tier_buffers)
    return int(total_connections)


def make_table(gigabyte_rows, idle_ratio_columns):
    table_rows = []
    for gigabytes in gigabyte_rows:
        table_columns = []
        for idle_ratio in idle_ratio_columns:
            table_columns.append(max_connections(gigabytes, idle_ratio))
        table_rows.append(table_columns)
    return table_rows


def generate_csv(gigabyte_rows, idle_ratio_columns):
    table_rows = make_table(gigabyte_rows, idle_ratio_columns)
    csv = ""
    for idle_ratio in idle_ratio_columns:
        csv += ',' + "%d%%" % (idle_ratio * 100)
    csv += '\n'

    row_index = 0
    for row in table_rows:
        csv += "%.1f" % gigabyte_rows[row_index]
        for column in row:
            csv += ",%d" % column
        csv += '\n'
        row_index += 1

    return csv


def build():
    ##
    ## Columns: Idle ratios
    ##
    cols = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)

    ##
    ## Rows: Gigabytes of memory provided
    ##
    rows = (0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 6.0, 8.0, 12.0, 16.0, 24.0, 32.0, 48.0, 64.0)

    csv = generate_csv(rows, cols)
    print(csv)


build()


