# Makefile

# Variables
CONTAINER_NAME = air-link
HOST_PORT = 8000

build:
	docker build -t $(CONTAINER_NAME) .
run:
	docker run --rm --env-file .env  -d -p $(HOST_PORT):8000 --name $(CONTAINER_NAME) $(CONTAINER_NAME)
stop:
	docker stop $(CONTAINER_NAME)
clean:
	docker rm $(CONTAINER_NAME)
	docker rmi $(CONTAINER_NAME)
logs:
	docker logs $(CONTAINER_NAME)
