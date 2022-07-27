#!/bin/bash

USER_MODE=1
LOCAL_IMAGE=0


while [[ $# -gt 0 ]]; do
  case $1 in
    -r|--root)
        USER_MODE=0
        shift # past argument
        ;;
    -l|--local)
        LOCAL_IMAGE=1
        shift # past argument
        ;;
    *)
        shift # past argument
        ;;
  esac
done


[ -z $IMAGE_PPAPERWORK ] && IMAGE_PPAPERWORK="ghcr.io/projectpaperwork/ppaperwork:latest"
if [ $LOCAL_IMAGE == 1 ] ; then
        echo "<!-- RUN LOCAL IMAGE -->"
        IMAGE_PPAPERWORK="ppaperwork"
fi;


if [ $USER_MODE == 1 ] ; then
        docker run \
        -v $(pwd):/workdir \
        -e USER_ID=$(id -u) \
        -e GROUP_ID=$(id -g) \
	-e TIMEZONE=$(cat /etc/timezone) \
        $IMAGE_PPAPERWORK bash work.sh
else
        echo "<!-- RUN AS ROOT -->"
        docker run --rm \
        -v $(pwd):/workdir \
        -e USER_ID=0 \
        $IMAGE_PPAPERWORK bash work.sh
fi;
