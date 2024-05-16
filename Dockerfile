FROM python:3

COPY target.zip /
RUN unzip target.zip

WORKDIR /target

RUN pip install --upgrade setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

CMD /bin/sh -c "echo hello stdout ; echo hello stderr >&2"