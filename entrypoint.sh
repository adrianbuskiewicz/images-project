#!/bin/bash
set -e

python manage.py loaddata images/fixtures/tier.json

exec "$@"