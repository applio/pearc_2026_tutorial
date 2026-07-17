#!/usr/bin/env bash
set -euo pipefail

LOG_FILE="$(dirname "$0")/dragon-jupyter.log"
SETTINGS_FILE="$(dirname "$0")/settings.json"
export K8S_JUPYTER_TOKEN="dragon-vscode"

discover_uri() {
  jupyter notebook list 2>/dev/null \
    | awk '/^http:\/\// { print $1; exit }' \
    | sed -E 's#http://(localhost|0\.0\.0\.0):#http://127.0.0.1:#'
}

CURRENT_URI="$(discover_uri || true)"
if [[ -n "${CURRENT_URI}" ]]; then
  echo "dragon-jupyter already running"
else
  nohup dragon-jupyter >"$LOG_FILE" 2>&1 &

  for _ in {1..40}; do
    CURRENT_URI="$(discover_uri || true)"
    if [[ -n "${CURRENT_URI}" ]]; then
      break
    fi
    sleep 0.25
  done
fi

if [[ -z "${CURRENT_URI}" ]]; then
  CURRENT_URI="http://127.0.0.1:8888/?token=${K8S_JUPYTER_TOKEN}"
fi

# Guarantee the URI includes a token so VS Code can connect non-interactively.
if [[ "${CURRENT_URI}" != *"token="* ]]; then
  if [[ "${CURRENT_URI}" == *"?"* ]]; then
    CURRENT_URI="${CURRENT_URI}&token=${K8S_JUPYTER_TOKEN}"
  else
    CURRENT_URI="${CURRENT_URI}?token=${K8S_JUPYTER_TOKEN}"
  fi
fi

if [[ -f "$SETTINGS_FILE" ]]; then
  sed -i -E "s#(\"jupyter\.jupyterServerURI\"[[:space:]]*:[[:space:]]*\").*(\")#\1${CURRENT_URI}\2#" "$SETTINGS_FILE"
  sed -i -E "s#(\"jupyter\.jupyterServerUri\"[[:space:]]*:[[:space:]]*\").*(\")#\1${CURRENT_URI}\2#" "$SETTINGS_FILE"

  if ! grep -q '"jupyter\.jupyterServerUri"' "$SETTINGS_FILE"; then
    sed -i -E "s#(\"jupyter\.jupyterServerURI\"[[:space:]]*:[[:space:]]*\"[^\"]+\",)#\1\n  \"jupyter.jupyterServerUri\": \"${CURRENT_URI}\",#" "$SETTINGS_FILE"
  fi
fi

echo "dragon-jupyter ready"
echo "$CURRENT_URI"
