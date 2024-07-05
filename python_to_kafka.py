from kafka import KafkaProducer, KafkaConsumer
import json
from dotenv import load_dotenv
import os
import logging



logging.basicConfig(level=logging.INFO)



def KafkaConsume(target_topic, bootstrap_servers):
    consumer = KafkaConsumer(
        target_topic,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset='latest', # earliest
        enable_auto_commit=True,
        group_id='my-group',  
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Deserialize messages from JSON
    )


    try:
        for message in consumer:
            logging.info(f"Message consumed from topic topic: {message.topic} key: {message.key} value:{message.value}")
    except Exception as e:
        logging.error(f"Failed to consume message: {e}")



def kafkaProduce(bootstrap_servers: str, security_protocol: str,target_topic: str, events_file :str):
    producer =  KafkaProducer(
        bootstrap_servers=bootstrap_servers,
        key_serializer=str.encode,
        security_protocol=security_protocol,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    

    with open(events_file,'r') as f:
        data = json.load(f)

        for o in data:
            logging.info(f"key:{o['key']}, value:{o['value']}")


            producer.send(
                topic=target_topic,
                key=o['key'],
                value=o['value']
            )

    
        producer.flush(timeout=20)
        producer.close(timeout=20)



if __name__ == '__main__':
    
    load_dotenv('./.env')

    runenv = os.getenv('ENV')
    bootstrap_servers = os.getenv('BOOTSTRAP_SERVERS')
    deals_target_topic = os.getenv('DEALS_TARGET_TOPIC')
    transactions_target_topic = os.getenv('TRANSACTIONS_TARGET_TOPIC')
    

    if runenv == "local":
        security_protocol = "PLAINTEXT"
    else: 
        security_protocol = "SSL"

    logging.info(f" runenv: {runenv}, bootstrap_servers: {bootstrap_servers},deals_target_topic: {deals_target_topic}, transactions_target_topic: {transactions_target_topic} ")
    

    kafkaProduce(bootstrap_servers, security_protocol, deals_target_topic, './events_deals.json')
    kafkaProduce(bootstrap_servers, security_protocol, transactions_target_topic, './events_transactions.json', )
    #KafkaConsume(deals_target_topic, bootstrap_servers)