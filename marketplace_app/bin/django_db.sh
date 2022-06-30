#!/usr/bin/env bash

# может возникать проблема при заведении бд в тестах, тестовому пользователю необходимо явно выдать права

# DATABASES["TEST"]["USER"]
DB_USER='test_user'

psql -U postgres -c "CREATE ROLE $DB_USER ;"
psql -U postgres -c "ALTER USER $DB_USER CREATEDB ;"
