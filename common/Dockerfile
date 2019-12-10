
FROM ubuntu:18.04

RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y -q --no-install-recommends nginx python3-tornado python3-kafka python3-urllib3 python3-requests python3-psutil python3-kazoo && rm -rf /var/lib/apt/lists/*;

COPY    *.py /home/
