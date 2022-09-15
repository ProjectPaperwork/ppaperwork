#!/bin/bash

USER_MODE=1
LOCAL_IMAGE=0
DOX_HTML_SERVER=0
DOX_SERVER_DETACH=0

# Argument parser
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
    -s|--serve)
        DOX_HTML_SERVER=1
        shift # past argument
        ;;

    -d|--detach)
        DOX_SERVER_DETACH=1
        shift
        ;;
    *)
        shift # past argument
        ;;
  esac
done


if [ $DOX_HTML_SERVER == 1 ] ; then
        DOX_SERVER_NAME="ppaperwork-dox-server-$USER"
        DOX_SERVER_ARGS=""
        DOX_SERVER_PORT="8080"

        if [ $DOX_SERVER_DETACH -eq 1 ] ; then
            DOX_SERVER_ARGS="-d"
        fi

        # Run an http server to be able to watch the doxygen html from a remote server
        echo "<!-- RUN HTTP SERVER PORT 8080 -->"
        docker run $DOX_SERVER_ARGS --rm --name $DOX_SERVER_NAME -v $PWD/documentation/doxygen/html:/usr/share/nginx/html:ro -p $DOX_SERVER_PORT:80 nginx
        server_ok=$?

        if [ $DOX_SERVER_DETACH -eq 1 ] ; then
            if [ $server_ok -eq 0 ] ; then
                echo ">> Server started as '$DOX_SERVER_NAME' on port $DOX_SERVER_PORT! use 'docker stop $DOX_SERVER_NAME' to stop"
            fi
        fi
else

        # Run the local image of ppaperwork (for dev purpose)
        [ -z $IMAGE_PPAPERWORK ] && IMAGE_PPAPERWORK="ghcr.io/projectpaperwork/ppaperwork:latest"
        if [ $LOCAL_IMAGE == 1 ] ; then
                echo "<!-- RUN LOCAL IMAGE -->"
                IMAGE_PPAPERWORK="ppaperwork"
        fi;

        # Run ppaperwork
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

fi;

