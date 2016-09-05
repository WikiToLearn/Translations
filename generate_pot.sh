#!/bin/bash

# Extract strings
ini2po -P ini templates

# Update translations
pot2po -t po-it/ templates/ po-it/

# Generate ini files
po2ini -t ini po-it it
