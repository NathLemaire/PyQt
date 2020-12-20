
FROM ubuntu:20.04

MAINTAINER jozo <hi@jozo.io>

ENV DEBIAN_FRONTEND=noninteractive

# Add user
RUN adduser --quiet --disabled-password qtuser && usermod -a -G audio qtuser

# This fix: libGL error: No matching fbConfigs or visuals found
ENV LIBGL_ALWAYS_INDIRECT=1

# Install Python 3, PyQt5
RUN apt-get update && apt-get install -y python3-pyqt5 && apt-get install sqlite3

COPY *.py /
COPY ./db/recettes.bd /
COPY ./icones/*.png /icones/

CMD ["python3", "principalSqlite.py"]
