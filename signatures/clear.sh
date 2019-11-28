#!/usr/bin/env bash

# rm temp file command 
find . -maxdepth 1 -type f -not -name "*.py" -not -name "1.txt" -not -name "pic.jpg" -not -name "*.sh" -print0 | xargs -0 rm