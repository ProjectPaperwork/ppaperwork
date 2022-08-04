#!/bin/bash

USER_ID=${USER_ID:-30000}
GROUP_ID=${GROUP_ID:-30000}
TIMEZONE=${TIMEZONE:UTC}

echo "Set timezone to ${TIMEZONE}"
setup-timezone -z ${TIMEZONE}

# Get version from git
git config --global --add safe.directory '*'
export PROJECT_VERSION_GIT_TAG=$(git tag --points-at HEAD | head -n 1)
echo "Version (first current git tag) : $PROJECT_VERSION_GIT_TAG"

# script is ran as root, so root!
if [ "$USER_ID" == 0 ]; then
	# We shall run everything as root
	mkdir -p /builder

	GOSU=""

# Host user has already the correct uid
elif [ "$USER_ID" == "$UID" ]; then
	GOSU=""

# Host user and container user don't have the same UID, so create a specific user
else
	addgroup -g ${GROUP_ID} builder
	adduser -D -G builder -u ${USER_ID} -h /builder builder
	GOSU="gosu builder"
fi

if [ "$PWD" = / ]; then
	cd /builder || exit 1
fi

cmd="python3 -u -m gherkin_paperwork"
echo "run cmd $cmd" 
exec $GOSU bash -c "$cmd"; 


