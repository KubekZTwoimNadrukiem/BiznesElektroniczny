#!/bin/bash
# # Wygenerowane przez ChatGPT.
# set -e
# echo "Importing database dump..."
# # Environment variables
# DB_HOST=${DB_SERVER:-mysql}
# DB_PORT=${DB_PORT:-3306}
# DB_USER=${DB_USER:-root}
# DB_PASSWORD=${DB_PASSWD:-root}
# DB_NAME=${DB_NAME:-prestashop}

# # Path to the dump file
#DUMP_FILE="/tmp/sql/dump.sql"

# # Wait for the database to be ready
# echo "Waiting for database to be ready..."
# until nc -z -v -w30 $DB_HOST $DB_PORT; do
#     echo "Waiting for database connection on $DB_HOST:$DB_PORT..."
#     sleep 5
# done
# echo "Database is ready!"

# # Import the dump
# if [ -f "$DUMP_FILE" ]; then
#     echo "Importing database dump..."
#     mysql -h $DB_HOST -P $DB_PORT -u $DB_USER -p$DB_PASSWORD $DB_NAME < $DUMP_FILE
#     echo "Database import completed!"
# else
#     echo "Database dump file not found at $DUMP_FILE!"
#     exit 1
# fi

# echo "Database import completed!"
# echo "Done" > /tmp/done.txt

mysql -u"$DB_USER" -p"$DB_PASSWD" -h"$DB_SERVER" "$DB_NAME" < /tmp/sql/dump.sql