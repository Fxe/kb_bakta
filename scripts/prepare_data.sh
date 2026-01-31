#!/usr/bin/env bash
set -euo pipefail

DATA_DIR="/data"
READY_FILE="${DATA_DIR}/__READY__"
URL="https://zenodo.org/records/14916843/files/db.tar.xz?download=1"
ARCHIVE="/tmp/db.tar.xz"

echo "Preparing data directory..."

# Create /data if it doesn't exist
mkdir -p "${DATA_DIR}"

# Download archive if not already present
if [ ! -f "${ARCHIVE}" ]; then
    echo "Downloading dataset..."
    curl -sSL -C - --retry 10 --retry-all-errors --retry-delay 5 \
        --connect-timeout 30 --max-time 0 "${URL}" -o "${ARCHIVE}"
else
    echo "Archive already downloaded, skipping download."
fi

# Extract into /data
echo "Extracting dataset to ${DATA_DIR}..."
tar -xJf "${ARCHIVE}" -C "${DATA_DIR}"

touch "${READY_FILE}"
echo "Reference data successfully prepared. READY file created."
