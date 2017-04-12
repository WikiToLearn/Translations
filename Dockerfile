FROM wikitolearn/python35:0.1

RUN apt-get update
RUN apt-get install -y translate-toolkit && \
  find /var/log/ -type f -delete && \
  rm -f /var/cache/apt/archives/*deb
RUN apt-get install -y subversion && \
  find /var/log/ -type f -delete && \
  rm -f /var/cache/apt/archives/*deb

ADD ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ADD ./Tool-MW-json/   /srv/Tool-MW-json/
ADD ./Tool-WikiPages/ /srv/Tool-WikiPages/
ADD ./DockerScripts/  /srv/DockerScripts/

RUN mkdir /etc/translations/

ENTRYPOINT /srv/DockerScripts/app.py
