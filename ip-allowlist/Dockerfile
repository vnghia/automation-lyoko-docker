FROM python:3.11.3-slim-bullseye

COPY ip-allowlist.py /usr/bin/ip-allowlist
COPY server.py /usr/bin/ip-allowlist-server

ENV IP_ALLOWLIST_DATA_PATH=/ip-allowlist/data.json
ENV IP_ALLOWLIST_GENERATE_PATH=/traefik/ip-allowlist.toml

RUN pip install tomlkit
RUN mkdir -p /ip-allowlist/ \
  && mkdir -p /traefik/ \
  && echo '{"127.0.0.1": "localhost"}' > $IP_ALLOWLIST_DATA_PATH
RUN /usr/bin/ip-allowlist ls
CMD [ "/usr/bin/ip-allowlist-server", "-p", "{{ ip_allowlist_port }}" ]
