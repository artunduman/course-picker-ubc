TAG=1.0.0

.PHONY: build
	build: export TAG
	build: docker-compose build coursepicker
