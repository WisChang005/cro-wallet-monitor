#! /bin/bash

FILEDIR=$(dirname "$0")

PYENV_PATH=".venv"

if [ ! -d "${PYENV_PATH}" ]; then
    echo -e "To create python venv"
    python3 -m venv ${PYENV_PATH}
fi

source ${PYENV_PATH}/bin/activate \
    && python -m pip install --upgrade pip \
    && pip install -r "${FILEDIR}/requirements.txt" \
    && source ~/.wisky_env \
    && python "${FILEDIR}/cro_wallet_monitor.py"