# skupper-tcp-sizing

This repo contains a script to compute sizing tables for TCP connections.

To run the script, simply use the command `python sizing.py > table.csv`

This will create a file (table.csv) that contains the generated comma-separated values than can be inserted into a spreadsheet.

To modify the table, edit the `build()` function with different column/row sets.  The Columns are values from 0.0 to 1.0.  The rows are memory sizes in units of Gigabytes.

The values in the table are maximum numbers of concurrently open TCP service connections with endpoints on a Skupper Router based on the amount of memory allocated to the router process.  Note that this calculation does not take into account the baseline memory usage of the idle router process.  For realistic memory allocations, this is a valid approximation.  For actual sizing, one would be well advised to inflate the number of expected connections by 20% or so to allow for error or growth.
