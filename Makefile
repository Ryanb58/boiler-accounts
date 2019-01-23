build:
	docker build --tag=accounts .

tag:
	docker tag accounts:latest ryanb58/boiler-accounts:latest

push:
	docker push ryanb58/boiler-accounts:latest

