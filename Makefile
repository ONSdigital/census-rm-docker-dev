DOT := $(shell command -v dot 2> /dev/null)

up:
	docker-compose -f dev.yml -f rm-services.yml up -d ${SERVICE} ;
	pipenv install --dev
	pipenv run python setup_database.py
	./setup_pubsub.sh
	pipenv run python setup_rabbit.py

down:
	docker-compose -f dev.yml -f rm-services.yml down

pull:
	docker-compose -f dev.yml -f rm-services.yml pull ${SERVICE}

logs:
	docker-compose -f dev.yml -f rm-services.yml logs --follow ${SERVICE}

diagrams: ensure-graphviz download-plantuml
	java -jar plantuml.jar -tsvg diagrams/*.puml

clean:
	rm -f plantuml.jar; rm -f diagrams/*.svg

download-plantuml:
ifeq (,$(wildcard plantuml.jar))
	curl -L --output plantuml.jar https://downloads.sourceforge.net/project/plantuml/plantuml.jar
endif 

ensure-graphviz:
ifndef DOT
	$(error "The dot command is not available - please install graphviz (brew install graphviz)")
endif
