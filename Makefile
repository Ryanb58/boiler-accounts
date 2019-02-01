build:
	docker build --tag=accounts .

tag:
	docker tag accounts:latest ryanb58/boiler-accounts:latest

push:
	docker push ryanb58/boiler-accounts:latest

run:
	docker run -it -p 80:80 accounts

run-local:
	docker run -it -p 80:80 ryanb58/boiler-accounts:latest
