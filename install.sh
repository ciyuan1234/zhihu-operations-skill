#!/usr/bin/env bash
#
# Zhihu Operations Skill Installer
# Compatible with macOS, Linux, and WSL
#
set -euo pipefail

SKILL_NAME="zhihu-operations"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="${SCRIPT_DIR}/${SKILL_NAME}"

echo "=========================================================="
echo " Zhihu Operations Skill Installer"
echo "=========================================================="

if [ ! -d "${SOURCE_DIR}" ]; then
  echo "[-] Error: Source directory '${SOURCE_DIR}' not found!"
  exit 1
fi

TARGET_BASE="${HOME}/.hermes/skills/social-media"
if [ -n "${1:-}" ]; then
  TARGET_DIR="$1"
else
  TARGET_DIR="${TARGET_BASE}/${SKILL_NAME}"
fi

echo "[*] Source: ${SOURCE_DIR}"
echo "[*] Target: ${TARGET_DIR}"

mkdir -p "$(dirname "${TARGET_DIR}")"

# Copy skill directory
if [ -d "${TARGET_DIR}" ]; then
  echo "[!] Existing skill directory found, updating..."
  rm -rf "${TARGET_DIR}"
fi

cp -R "${SOURCE_DIR}" "${TARGET_DIR}"

# Ensure scripts are executable
chmod +x "${TARGET_DIR}/scripts/"*.py 2>/dev/null || true

echo "[+] Successfully installed ${SKILL_NAME} to: ${TARGET_DIR}"
echo ""
echo "Verify installation:"
echo "  python3 \"${TARGET_DIR}/scripts/lint.py\" --help"
echo "  python3 \"${TARGET_DIR}/scripts/guard.py\" check"
echo "  python3 \"${TARGET_DIR}/scripts/question_evaluator.py\" --help"
echo ""
echo "In Hermes Agent:"
echo "  skill_view(name='zhihu-operations')"
echo "=========================================================="
