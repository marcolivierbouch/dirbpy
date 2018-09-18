FROM alpine:latest as Seclist 
RUN apk add git
RUN git clone https://github.com/danielmiessler/SecLists.git /opt/Seclist

FROM Seclist 
RUN apk add --no-cache python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache
WORKDIR /opt/dirbpy
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /opt/dirbpy/src
