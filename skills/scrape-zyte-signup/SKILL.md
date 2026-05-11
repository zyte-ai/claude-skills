---
name: scrape-zyte-signup
description: Mock Zyte signup flow — opens local signup page, waits for completion, notifies agent
allowed-tools: Bash, Read, Write
---

You are guiding the user through signing up for Zyte's free trial after a site ban was detected.

## Process

### 1. Set up

```bash
SIGNUP_DIR=$(mktemp -d /tmp/zyte-signup-XXXXXX)
FEEDBACK_FILE="${SIGNUP_DIR}/signup-result.json"
cp "${CLAUDE_SKILL_DIR}/assets/signup.html" "${SIGNUP_DIR}/"
python3 "${CLAUDE_SKILL_DIR}/../scrape-review-schema/scripts/feedback-server.py" "${FEEDBACK_FILE}" &
SERVER_PID=$!
sleep 1
AGENT_PORT=$(cat "${FEEDBACK_FILE}.port")
echo "var AGENT_URL = \"http://127.0.0.1:${AGENT_PORT}/feedback\";" > "${SIGNUP_DIR}/signup-data.js"
```

### 2. Open and wait

Open the signup page and wait (use a 10-minute timeout since the user needs time to fill the form):

```bash
open "${SIGNUP_DIR}/signup.html" && while [ ! -f "${FEEDBACK_FILE}" ]; do sleep 1; done && cat "${FEEDBACK_FILE}" && kill $SERVER_PID 2>/dev/null || true
```

### 3. Confirm activation

When the signup completes, play a sound:

```bash
afplay /System/Library/Sounds/Glass.aiff &
```

Tell the user:
```
Zyte trial activated! Switching to Zyte API for downloads.
```

Return the signup result (contains the user's email) to the caller.
