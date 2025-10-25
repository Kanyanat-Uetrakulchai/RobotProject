#!/usr/bin/env bash
THIS_DIR="$( cd -- "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export GZ_SIM_RESOURCE_PATH="$THIS_DIR/World/models:${GZ_SIM_RESOURCE_PATH}"
echo "[OK] GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH"
