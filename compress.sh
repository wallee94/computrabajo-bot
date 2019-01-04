#!/usr/bin/env bash

rm -f lambda_function.zip
cd venv/lib/python3*/site-packages
zip -r9 ../../../../lambda_function.zip .
cd ../../../../
zip -g lambda_function.zip lambda*