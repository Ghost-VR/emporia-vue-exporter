DOCKER_IMAGE_NAME = ghostvr/emporia-vue-exporter
PLATFORM = linux/arm64,linux/amd64
CURRENT_TAG = 0.1.x

docker_build:
	docker build --platform $(PLATFORM) -t $(DOCKER_IMAGE_NAME) .

docker_run:
#	docker run -p 9090:9090 -v /host/path/secrets:/usr/src/app/secrets $(DOCKER_IMAGE_NAME) 
	docker run -p 9090:9090 $(DOCKER_IMAGE_NAME) 

docker_probe:
	docker run -i -t $(DOCKER_IMAGE_NAME) /bin/bash

docker_new_tag:
	docker tag $(DOCKER_IMAGE_NAME):latest $(DOCKER_IMAGE_NAME):$(CURRENT_TAG)

docker_push:
	docker push $(DOCKER_IMAGE_NAME):$(CURRENT_TAG)
	docker push $(DOCKER_IMAGE_NAME):latest
