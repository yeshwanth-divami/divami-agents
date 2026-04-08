---
name: gws-gmail-read
version: 1.1.0
description: "Gmail: Read a message and extract its body or headers."
metadata:
  openclaw:
    category: "productivity"
    requires:
      bins: ["gws"]
    cliHelp: "gws gmail users messages get --help"
---

# gmail read (raw API)

> **PREREQUISITE:** Read `../gws-shared/SKILL.md` for auth, global flags, and security rules. If missing, run `gws generate-skills` to create it.

> ⚠️ **`gws gmail +read` does NOT exist in the binary.** The binary returns "unrecognized subcommand '+read'". Use the raw API call below instead.

Read a message and extract its body or headers using the raw API.

## Usage

```bash
# Fetch full message (headers + body)
gws gmail users messages get --params '{"userId":"me","id":"<MESSAGE_ID>","format":"full"}' --format json > /tmp/msg.json
```

## Extracting content with Python

The JSON output includes a `Using keyring backend: keyring` preamble line. Always skip it when parsing:

```python
import json, base64, subprocess

result = subprocess.run(
    ['gws', 'gmail', 'users', 'messages', 'get',
     '--params', '{"userId":"me","id":"<ID>","format":"full"}',
     '--format', 'json'],
    capture_output=True, text=True
)
lines = result.stdout.split('\n')
json_start = next(i for i, l in enumerate(lines) if l.strip().startswith('{'))
data = json.loads('\n'.join(lines[json_start:]))

headers = {h['name']: h['value'] for h in data['payload']['headers']}
print(headers.get('Subject'), headers.get('Date'))

def decode_part(part):
    b = part.get('body', {}).get('data', '')
    return base64.urlsafe_b64decode(b + '==').decode('utf-8', errors='replace') if b else ''

def extract_plain(payload):
    if payload.get('mimeType') == 'text/plain':
        return decode_part(payload)
    for p in payload.get('parts', []):
        t = extract_plain(p)
        if t.strip():
            return t
    return ''

body = extract_plain(data['payload'])
```

## Key Notes

- The `<MESSAGE_ID>` must be a real API message ID (looks like `19d1dfa9890404f5`). See `gmail-meeting-mom` for how to obtain it.
- Save the output to `/tmp/` first with `> /tmp/msg.json`, then parse — do not pipe directly to a heredoc.
- Handles multipart/alternative and base64 decoding manually as shown above.

## See Also

- [gws-shared](../gws-shared/SKILL.md) — Global flags and auth
- [gws-gmail](../gws-gmail/SKILL.md) — All send, read, and manage email commands
