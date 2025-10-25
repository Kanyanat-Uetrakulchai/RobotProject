#!/usr/bin/env bash
THIS_DIR="$( cd -- "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

NEW_PATH="$THIS_DIR/World/models"


if [[ ":$GZ_SIM_RESOURCE_PATH:" != *":$NEW_PATH:"* ]]; then
    
    if [ -n "$GZ_SIM_RESOURCE_PATH" ]; then
        export GZ_SIM_RESOURCE_PATH="$NEW_PATH:$GZ_SIM_RESOURCE_PATH"
    else
        export GZ_SIM_RESOURCE_PATH="$NEW_PATH"
    fi
fi

echo "[OK] GZ_SIM_RESOURCE_PATH=$GZ_SIM_RESOURCE_PATH"