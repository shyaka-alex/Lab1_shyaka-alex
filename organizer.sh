#!/bin/bash

# organizer.sh
# Archives the current grades.csv into an archive/ folder with a timestamped
# filename, resets the workspace with a fresh empty grades.csv, and logs
# every run to organizer.log.

ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"
SOURCE_FILE="grades.csv"


if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
    echo "Created archive directory: $ARCHIVE_DIR"
fi


if [ ! -f "$SOURCE_FILE" ]; then
    echo "Error: '$SOURCE_FILE' not found in the current directory. Nothing to archive."
    exit 1
fi


TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
ARCHIVED_NAME="grades_${TIMESTAMP}.csv"


mv "$SOURCE_FILE" "$ARCHIVE_DIR/$ARCHIVED_NAME"


touch "$SOURCE_FILE"


LOG_TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
echo "[$LOG_TIMESTAMP] Archived '$SOURCE_FILE' -> '$ARCHIVE_DIR/$ARCHIVED_NAME'" >> "$LOG_FILE"

echo "Archived '$SOURCE_FILE' as '$ARCHIVE_DIR/$ARCHIVED_NAME'."
echo "A fresh, empty '$SOURCE_FILE' has been created."
echo "Action logged to '$LOG_FILE'."
