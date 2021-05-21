#!/usr/bin/env bash
mkdir -p _build
sphinx-build -c .github/ -b html ./ ./_build/
