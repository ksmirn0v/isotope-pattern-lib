#!/usr/bin/env bash
# Computes the next release version from a PR title ([MAJOR]/[MINOR]/[PATCH])
# and the latest existing "X.Y.Z" git tag. Prints the version to stdout.
set -euo pipefail

title="${1:?usage: compute-next-version.sh <pr-title>}"

if echo "$title" | grep -qi '\[major\]'; then
  bump="major"
elif echo "$title" | grep -qi '\[minor\]'; then
  bump="minor"
elif echo "$title" | grep -qi '\[patch\]'; then
  bump="patch"
else
  echo "PR title must contain one of [MAJOR], [MINOR], [PATCH]: '${title}'" >&2
  exit 1
fi

latest_tag=$(git tag --list | grep -E '^[0-9]+\.[0-9]+\.[0-9]+$' | sort -t. -k1,1n -k2,2n -k3,3n | tail -1 || true)

if [ -z "$latest_tag" ]; then
  if [ "$bump" != "major" ]; then
    echo "No existing release tag found; a [${bump}] PR cannot be the first release, only [MAJOR] can" >&2
    exit 1
  fi
  echo "1.0.0"
  exit 0
fi

IFS='.' read -r major minor patch <<< "$latest_tag"

case "$bump" in
  major)
    echo "$((major + 1)).0.0"
    ;;
  minor)
    echo "${major}.$((minor + 1)).0"
    ;;
  patch)
    echo "${major}.${minor}.$((patch + 1))"
    ;;
esac
