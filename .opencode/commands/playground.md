---
description: Start the SlopLang web playground in the background on a port (default 8080), reusing an existing Sloperator server if one is running
---

Start the Sloperator web playground on port $ARGUMENTS. If $ARGUMENTS is empty, use port 8080.

Current TCP listeners (`lsof -nP -iTCP -sTCP:LISTEN`):

!`lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null || true`

1. Determine the port: use $ARGUMENTS if it is a valid port number (1-65535), otherwise use 8080. If it is not a valid port, stop and report the problem.
2. Check the listener output above for anything already bound to that port.
   - If a Sloperator playground server (a Python process running `playground/server.py`) is already listening on that port, do not start another one. Report that it is already running at `http://localhost:<port>` and stop.
   - If a different process is listening on that port, do not kill it. Stop and report which process holds the port.
3. If the port is free, start the server in the background from the repo root with `uv run playground/server.py <port>`. Run it as a background command so it keeps running.
4. Wait a moment, then confirm it is listening with `lsof -nP -iTCP:<port> -sTCP:LISTEN`.
5. Report the URL `http://localhost:<port>` and how to stop it (Ctrl+C in its session, or kill the PID shown by `lsof`).
