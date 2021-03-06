#!/bin/bash

USER_ID=${USER_ID:-30000}
GROUP_ID=${GROUP_ID:-30000}

if [ "$USER_ID" == 0 ]; then
	# We shall run everything as root
	mkdir -p /builder

	GOSU=""
elif [ "$USER_ID" == "$UID" ]; then
	GOSU=""
else
	if ! grep -q "^builder:" /etc/group; then
		groupadd -o --gid "$GROUP_ID" builder
	fi
	if ! id builder >/dev/null 2>&1; then
		# Create a non-root user that will perform the actual build
		useradd -o --uid "$USER_ID" --gid "$GROUP_ID" --create-home \
			--home-dir /builder builder
	fi

	GOSU="gosu builder"
fi

if [ "$PWD" = / ]; then
	cd /builder || exit 1
fi

# if [[ -z "$@" ]]; then
#   echo "no cmd passed" 
# #   exec $GOSU bash
# else 
  cmd="python3 -m gherkin_paperwork"
  echo "run cmd $cmd" 
  exec $GOSU bash -c "$cmd"; 
# fi


