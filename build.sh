#!/bin/bash
set -e

# Install dependencies
pip install -r requirements.txt

# Run Alembic migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
