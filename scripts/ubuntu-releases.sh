#/bin/bash

fatal() {
  echo "$1"
  exit 1
}

warn() {
  echo "$1"
}

if [ ! -d "$TUNASYNC_WORKING_DIR" ]; then
    fatal "Directory not exists, fail"
fi

RSYNCSOURCE="$TUNASYNC_UPSTREAM_URL"
BASEDIR="$TUNASYNC_WORKING_DIR"

if [ ! -d ${BASEDIR} ]; then
  warn "${BASEDIR} does not exist yet, trying to create it..."
  mkdir -p ${BASEDIR} || fatal "Creation of ${BASEDIR} failed."
fi

{
rsync --verbose --recursive --times --links --hard-links \
  --stats --delete-after \
  ${RSYNCSOURCE} ${BASEDIR} || fatal "Failed to rsync from ${RSYNCSOURCE}."
} > $TUNASYNC_LOG_FILE

date -u > ${BASEDIR}/.trace/$(hostname -f)
