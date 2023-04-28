#!/usr/bin/env bash
set -euo pipefail

apt update && apt install -y --no-install-recommends nginx-full

rm -rf /etc/nginx/sites-enabled/default
rm -rf /etc/nginx/sites-available/default
