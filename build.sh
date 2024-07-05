ecr_repository=941154566110.dkr.ecr.us-east-1.amazonaws.com


docker build --platform linux/amd64 -t push_manual_events_to_kafka . && \
docker tag push_manual_events_to_kafka ${ecr_repository}/push_manual_events_to_kafka:latest && \
docker push ${ecr_repository}/push_manual_events_to_kafka:latest