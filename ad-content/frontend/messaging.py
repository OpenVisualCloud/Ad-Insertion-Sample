#!/usr/bin/python3

from kafka import KafkaProducer, KafkaConsumer, TopicPartition
import socket

kafka_hosts=["kafka-service:9092"]

class Producer(object):
    def __init__(self):
        super(Producer,self).__init__()
        self._client_id=socket.gethostname()
        self._producer=None

    def send(self,topic,message):
        if not self._producer:
            try:
                self._producer=KafkaProducer(bootstrap_servers=kafka_hosts,client_id=self._client_id,api_version=(0,10),retries=1)
            except Exception as e:
                print(str(e))
                self._producer=None

        if self._producer:
            try:
                self._producer.send(topic,message.encode('utf-8'))
                print("send "+topic+": ")
                print(message)
            except Exception as e:
                print(str(e))
        else:
            print("producer not available")

    def flush(self):
        if self._producer: self._producer.flush()

    def close(self):
        if self._producer: 
            self.flush()
            self._producer.close()

class Consumer(object):
    def __init__(self, group=None):
        super(Consumer,self).__init__()
        self._client_id=socket.gethostname()
        self._group=group

    def messages(self, topic, timeout=None):
        c=KafkaConsumer(topic, bootstrap_servers=kafka_hosts, client_id=self._client_id , group_id=self._group, api_version=(0,10))

        partitions=c.partitions_for_topic(topic)
        if not partitions: raise Exception("Topic "+topic+" not exist")

        timeout1=100 if timeout is None else timeout
        while True:
            partitions=c.poll(timeout1)
            if partitions:
                for p in partitions:
                    for msg in partitions[p]:
                        yield msg.value.decode('utf-8')
            if timeout is not None: yield ""

        c.close()

    def debug(self, topic):
        c=KafkaConsumer(bootstrap_servers=kafka_hosts, client_id=self._client_id , group_id=None, api_version=(0,10))

        # assign/subscribe topic
        partitions=c.partitions_for_topic(topic)
        if not partitions: raise Exception("Topic "+topic+" not exist")
        c.assign([TopicPartition(topic,p) for p in partitions])

        # seek to beginning if needed
        c.seek_to_beginning()

        # fetch messages
        while True:
            partitions=c.poll(100)
            if partitions:
                for p in partitions:
                    for msg in partitions[p]:
                        yield msg.value.decode('utf-8')
            yield ""

        c.close()
