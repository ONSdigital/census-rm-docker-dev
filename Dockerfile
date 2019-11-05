FROM rabbitmq:3.6.10-management
RUN rabbitmq-plugins enable rabbitmq_federation
RUN rabbitmq-plugins enable rabbitmq_federation_management


