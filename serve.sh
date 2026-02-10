#!/bin/bash
# Serve the Krypton NAS Dashboard
# Usage: ./serve.sh [port]

PORT=${1:-8080}
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Read project name from system.json if available
PROJECT_NAME="Krypton NAS"
if [ -f "$DIR/.state/system.json" ]; then
    NAME=$(python3 -c "import json; print(json.load(open('$DIR/.state/system.json')).get('name', 'Krypton NAS'))" 2>/dev/null)
    if [ -n "$NAME" ]; then
        PROJECT_NAME="$NAME"
    fi
fi

echo "========================================"
echo "  $PROJECT_NAME Dashboard"
echo "========================================"
echo ""
echo "Starting server at http://localhost:$PORT"
echo "Project directory: $DIR"
echo ""
echo "Available pages:"
echo "  - http://localhost:$PORT/dashboard/index.html       (Home)"
echo "  - http://localhost:$PORT/dashboard/overview.html    (Overview)"
echo "  - http://localhost:$PORT/dashboard/components.html  (Components)"
echo "  - http://localhost:$PORT/dashboard/features.html    (Features)"
echo "  - http://localhost:$PORT/dashboard/tasks.html       (Tasks)"
echo "  - http://localhost:$PORT/dashboard/changelog.html   (Changelog)"
echo "  - http://localhost:$PORT/dashboard/glossary.html    (Glossary)"
echo "  - http://localhost:$PORT/dashboard/spec-viewer.html (Spec Sheet)"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================"

cd "$DIR"
python3 -m http.server $PORT
