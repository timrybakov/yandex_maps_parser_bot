#!/bin/sh

poetry run celery -A src.celery worker --loglevel=info --pool=solo
