#!/usr/bin/env bash

# --------------------------------------------------------------------------------------------------
# test for docker using unittest
# --------------------------------------------------------------------------------------------------

python3 -W ignore:ResourceWarning -m unittest

# --------------------------------------------------------------------------------------------------
# check code coverage for local development
# --------------------------------------------------------------------------------------------------

#coverage run -m unittest
#coverage report --omit="*/lib*,*__init__.py"
#coverage html --omit="*/lib*,*__init__.py"

#touch /tmp/a.out
#tail -f /tmp/a.out
