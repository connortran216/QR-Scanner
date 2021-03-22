if [ -z $(docker network ls --filter name=^${DOCKER_INTERNAL_NETWORK}$ --format="{{ .Name }}") ] ; then
     docker network create ${DOCKER_INTERNAL_NETWORK} ;
fi

docker-compose up -d