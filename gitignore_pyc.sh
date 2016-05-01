#!/bin/bash
echo "Script execution started"
for dir in /Users/hacker/soham/django_apps/meetme/*; do (echo dir;git checkout *.pyc;git rm *.pyc);done
echo "Script completed"
