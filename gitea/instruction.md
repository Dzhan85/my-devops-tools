# Gitea

## Installation 

use docker compose file

```
version: "2"

networks:
  gitea:
    external: false

services:
  server:
    image: gitea/gitea:1.6.4
    environment:
      - USER_UID=1000
      - USER_GID=1000
      - DB_TYPE=postgres
      - DB_HOST=172.17.0.1:5432
      - DB_NAME=gitea
      - DB_USER=gitea
      - DB_PASSWD=gitea
      - ROOT_URL=https://cordelianew.university.innopolis.ru/gitea
    restart: always
    networks:
      - gitea
    volumes:
      - /srv/gitea:/data
    ports:
      - "3000:3000

```

## Backup and restore

Backups use the standard Gitea Backup 58 procedure adjusted for use with Docker as follows:

 Shell into the Docker container:

    docker exec -it $(docker ps -qf "name=gitea") bash

  Use gitea dump the create the backup archive within the container:

    /app/gitea/gitea dump -c /data/gitea/conf/app.ini

  Assumes /data is a volume mapped from the container to your host’s gitea directory.

  Exit the shell and use docker cp to copy the archive to the host:

    docker cp $(docker ps -qf "name=gitea"):/gitea-dump-1537778440.zip .

If your host machine does not, itself, have a backup process in place consider moving the backup 



### Creating a Backup

To create a gitea dump, connect to the docker container and get a bash shell as the user
git via the docker exec command:

#### 2-way - connect to gitea container

       docker exec -it --user git name_of_gitea_container /bin/bash

This will give you a bash shell as the user git. Now create a gitea dump file (the gitea dump command requires you to be in /app/gitea, this assumes that the gitea executable is at the default location of /app/gitea/gitea):

> necessary
> `cd /app/gitea`

#### create gitea dump

    /app/gitea/gitea dump --file gitea-dump.zip --skip-repository

IMPORTANT: The --skip-repositories flag means we are making the gitea dump way, way, way smaller, but it also means we need to back up and restore the repositories folder ourselves! (See below for instructions.)

Now copy the file out of the container, then remove it from the container:

#### copy gitea dump out of container

     docker cp name_of_gitea_container:/app/gitea/gitea-dump.zip .

#### remove gitea dump

     docker exec -it name_of_gitea_container rm /app/gitea/gitea-dump.zip

Contents of Dump File

When the gitea dump file is unzipped, it will create the following files:

  ```  app.ini
    custom/ directory
    log/ directory (useless duplicate, already contained in custom/ dir)
    data/ directory
```
These files should map to the following locations in the docker container running the live gitea instance:
```
gitea dump file:        gitea live instance:
----------------        --------------------
app.ini                 /data/gitea/conf/app.ini
custom/                 /data/gitea/
log/                    (useless duplicate of custom/log/)
data                    /app/gitea/data
```

## Restoring a Backup

To restore a backup, copy the following files from the gitea dump
to the following locations inside this repository:

```
gitea dump file:        d-gitea repo location:
----------------        ----------------------
app.ini                 d-gitea/custom/conf/app.ini
custom/*                d-gitea/custom/*
data                    d-gitea/data
````

(If you’re running pod-charlesreid1, put these files in the specified location in the d-gitea submodule.)

### Restoring repositories directory

Note that when we created the gitea dump, we excluded the repositories themselves.
This is because these will greatly inflate the size of our gitea dump and will make
it much more difficult to store our backup files.

Repository contents can be backed up separately as follows:

    Log in to the old server
    Back up the /data/git/repositories directory (copy and compress)
    Copy the backup to the new server
    Log in to the new server
    Mount the /data/git/repositories folder

Optionally, if you want to keep the repositories folder in its own location, modify docker-compose.yml to add the following line to the gitea container’s volumes configuration:
```
services:
  server:
    image: gitea/gitea:latest

    ...

    volumes:
      - "/path/to/repositories:/data/git/repositories"
    
    ...
```
This should make it easier to manage, back up, and restore the repositories folder.

Database backups

We opt for the SQLite backend for gitea, which means the database is kept in a flat file on disk called /data/gitea/gitea.db.

The location of this file and the format of the database are specified in the config file in d-gitea/custom/conf/app.ini.

This file should not be edited, instead change the Jinja template d-gitea/custom/conf/app.ini.j2 and remake app.ini from the template.





---

## Sources

1. https://posts.specterops.io/attacking-freeipa-part-iii-finding-a-path-677405b5b95e


2. https://git.charlesreid1.com/docker/d-gitea/src/branch/master/docs/index.md
3. https://docs.gitea.io/en-us/backup-and-restore/