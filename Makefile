DOCKER_IMAGE_NAME = ghostvr/emporia-vue-exporter
PLATFORM = linux/arm64,linux/amd64

docker_build:
	docker build --platform $(PLATFORM) -t $(DOCKER_IMAGE_NAME) .

docker_run:
	docker run $(DOCKER_IMAGE_NAME)

docker_probe:
	docker run -i -t $(DOCKER_IMAGE_NAME) /bin/bash

docker_push:
	docker push $(DOCKER_IMAGE_NAME):latest
