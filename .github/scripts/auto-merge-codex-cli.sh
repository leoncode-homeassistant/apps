#!/usr/bin/env bash
set -euo pipefail

: "${GITHUB_REPOSITORY:?}"
: "${PR_NUMBER:?}"

# Fail closed until GitHub is configured to require all three checks.
protection="$(gh api "repos/$GITHUB_REPOSITORY/branches/main/protection/required_status_checks")"
for check in \
    'Lint codex-cli' \
    'Build codex-cli / Build codex-cli for amd64' \
    'Build codex-cli / Build codex-cli for aarch64'; do
    jq -e --arg check "$check" \
        '([.contexts[]?, .checks[]?.context] | index($check)) != null' \
        <<< "$protection" >/dev/null
done
jq -e '.strict == true' <<< "$protection" >/dev/null

pr="$(gh pr view "$PR_NUMBER" --repo "$GITHUB_REPOSITORY" \
    --json headRefName,headRefOid,baseRefName,isCrossRepository,author,state)"
jq -e '.headRefName == "automation/update-codex-cli" and .baseRefName == "main"
    and .isCrossRepository == false and .state == "OPEN"
    and .author.login == "app/github-actions"' <<< "$pr" >/dev/null
head_sha="$(jq -r .headRefOid <<< "$pr")"

gh pr merge "$PR_NUMBER" --repo "$GITHUB_REPOSITORY" --auto --squash \
    --match-head-commit "$head_sha"

# GITHUB_TOKEN merges may not trigger push workflows. Explicitly publish after
# GitHub reports the merge; never publish an unmerged update branch.
for ((attempt=0; attempt<120; attempt++)); do
    state="$(gh pr view "$PR_NUMBER" --repo "$GITHUB_REPOSITORY" --json state --jq .state)"
    if [[ "$state" == MERGED ]]; then
        gh workflow run builder.yaml --repo "$GITHUB_REPOSITORY" --ref main \
            -f app=codex-cli -f publish=true
        exit 0
    fi
    if [[ "$state" == CLOSED ]]; then
        echo 'Update PR was closed without merging.' >&2
        exit 1
    fi
    sleep 15
done
echo 'PR is still open after 30 minutes; inspect its required checks and auto-merge status.' >&2
exit 1
