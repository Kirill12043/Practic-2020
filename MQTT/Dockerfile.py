От python:3.8
ENV DEBIAN_FRONTEND неинтерактивный
WORKDIR / usr / src / app
Запустить apt-get update & & apt-get install-y python3-pip & & pip3 установить колбу matplotlib influxdb\
 && apt-get install-y python3-tk 
Копировать prog / / usr / src / app / prog
CMD ["python3", "- m", "prog"]
