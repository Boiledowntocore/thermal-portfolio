#!/usr/bin/env bash
# Move the site to a new GitHub Pages origin, in the one order that works.
#
# Run AFTER the GitHub username has been changed in web settings.
# Usage:  bash tools/switch_domain.sh princechauhan-thermal
#
# Naming the repo "<username>.github.io" is what makes GitHub serve it at the
# root (https://<username>.github.io/) instead of under a /repo-name path.
# It only works while the repo name matches the username exactly — which is why
# the username has to change first.

set -euo pipefail

USER_NEW="${1:?usage: switch_domain.sh <new-github-username>}"
REPO_NEW="${USER_NEW}.github.io"
URL_NEW="https://${USER_NEW}.github.io/"

echo "==> target: ${URL_NEW}"

# 1. Confirm the username rename actually happened. Renaming the repo first
#    would leave it as a project site at a nested path.
if ! curl -sf -o /dev/null "https://api.github.com/users/${USER_NEW}"; then
  echo "STOP: GitHub user '${USER_NEW}' does not exist yet."
  echo "      Change the username at https://github.com/settings/admin first."
  exit 1
fi

CUR_REPO="$(gh repo view --json nameWithOwner -q .nameWithOwner)"
echo "==> current repo: ${CUR_REPO}"

# 2. Rename the repo so it becomes the user site.
gh repo rename "${REPO_NEW}" --yes
echo "==> renamed to ${USER_NEW}/${REPO_NEW}"

# 3. Repoint the local remote. The old URL still redirects, but leaving it
#    stale means the next person to clone gets a surprise.
git remote set-url origin "https://github.com/${USER_NEW}/${REPO_NEW}.git"

# 4. Rewrite the link-preview tags. A stale absolute og:image does not fall
#    back to anything — the card silently renders blank.
python - "$URL_NEW" <<'PY'
import io, re, sys
url = sys.argv[1]                      # e.g. https://name.github.io/
p = "index.html"
s = io.open(p, encoding="utf-8").read()
# Replace the whole old origin AND any repo path segment. A user site lives at
# the root, so the previous /<repo>/ prefix must be dropped, not carried over.
s = re.sub(r'https://[A-Za-z0-9.-]+\.github\.io/(?:[^"]*?/)?(?=assets/|")', url, s)
io.open(p, "w", encoding="utf-8").write(s)
print("   og/twitter tags ->", url)
PY

grep -oE 'content="https://[^"]*"' index.html || true

git add -A
git commit -q -m "Move to ${URL_NEW}

Repo renamed to <username>.github.io so Pages serves it at the root.
Link-preview tags repointed; a stale absolute og:image renders no card at all.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>"
git push -q origin main

echo "==> pushed. Pages will rebuild in ~1 min."
echo "==> then verify:  curl -sI ${URL_NEW} | head -1"
