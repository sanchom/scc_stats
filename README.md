This script gets the list of appeals for a given calendar year, then
checks the docket for the list of interveners in each case. It prints
a markdown-formatted output summarizing this info. The output can be
viewed [here](interveners-2009-2018.md).

The `.pkl` file is a cache of info already downloaded from the SCC,
but if you want to retrieve fresh data, just delete the `.pkl` file.

The Dockerfile provides an environment that you can run this all in.
