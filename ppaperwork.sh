
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


echo $USER_MODE
echo $LOCAL_IMAGE


IMAGE_PPAPERWORK="ghcr.io/xdoctorwhoz/ppaperwork:latest"
if [ $LOCAL_IMAGE == 1 ] ; then
        IMAGE_PPAPERWORK="ppaperwork"
fi;


if [ $USER_MODE == 1 ] ; then
        docker run \
        -v $(pwd):/workdir \
        -e USER_ID=$(id -u) \
        -e GROUP_ID=$(id -g) \
        $IMAGE_PPAPERWORK
else
        docker run \
        -v $(pwd):/workdir \
        -e USER_ID=0 \
        $IMAGE_PPAPERWORK
fi;
