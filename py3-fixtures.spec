### RPM external py3-fixtures 3.0.0
## IMPORT build-with-pip3

Requires: py3-pbr py3-six py3-testtools
%define PipPostBuild perl -p -i -e "s|^#!.*python|#!/usr/bin/env python|" %{i}/bin/*
