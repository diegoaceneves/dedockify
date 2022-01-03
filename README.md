# dedockify

Reverse Engineering on Docker Image

## Running

### Start a new virtual enviroment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependences

```bash
pip install -r requirements.txt
```

### Getting image id

```bash
docker image ls
REPOSITORY                              TAG       IMAGE ID       CREATED        SIZE
golang                                  latest    276895edf967   9 days ago     941MB
debian                                  latest    6f4986d78878   10 days ago    124MB
alpine                                  latest    c059bfaa849c   5 weeks ago    5.59MB
ubuntu                                  latest    ba6acccedd29   2 months ago   72.8MB
diegoaceneves/mysqldump                 latest    9b4725482522   8 months ago   188MB

```

### Getting Dockerfile

```bash
python3 dedockify.py -i 9b4725482522
FROM diegoaceneves/mysqldump:latest
ADD file:c855b3c65f5ba94d548d7d2659094eeb63fbf7f8419ac8e07712c3320c38b62c in /
CMD ["bash"]
RUN /bin/sh -c apt-get update \
    && apt-get upgrade -y \
    && apt-get install mariadb-client-10.3 bzip2  -y
ENV DB_NAME=mysql
ENV DB_USER=root
ENV DB_PASS=pass
ENV DB_HOST=localhost
WORKDIR /backup
CMD ["/bin/sh" "-c" "/usr/bin/mysqldump -h$DB_HOST -u$DB_USER -p$DB_PASS $DB_NAME > $DB_NAME.sql"]
```

### Running with a different docker socket

By default, this script uses `unix://var/run/docker.sock` as docker socket file, if is necessary, can be used a different one passing by argument in execution time:

```bash
python3 dedockify.py -i 9b4725482522 -b unix://var/run/docker.sock
FROM diegoaceneves/mysqldump:latest
ADD file:c855b3c65f5ba94d548d7d2659094eeb63fbf7f8419ac8e07712c3320c38b62c in /
CMD ["bash"]
RUN /bin/sh -c apt-get update \
    && apt-get upgrade -y \
    && apt-get install mariadb-client-10.3 bzip2  -y
ENV DB_NAME=mysql
ENV DB_USER=root
ENV DB_PASS=pass
ENV DB_HOST=localhost
WORKDIR /backup
CMD ["/bin/sh" "-c" "/usr/bin/mysqldump -h$DB_HOST -u$DB_USER -p$DB_PASS $DB_NAME > $DB_NAME.sql"]
```
