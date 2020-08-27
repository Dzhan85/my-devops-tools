# OwnCloud

This manual is customized for Autonomous Transport System Lab. Official ownCloud manual resides [here](https://doc.owncloud.com/server/). 

## Installation

1. Create a new project directory **owncloud-docker-server**:
`$ mkdir /home/robolab/owncloud-docker-server`
`$ cd /home/robolab/owncloud-docker-server`

2. Create **docker-compose.yml**:
`$ vim docker-compose.yml`

3. Fill **docker-compose.yml** file:

   ```
   version: '2.1'
 
   volumes:
     mysql:
       driver: local
     redis:
       driver: local
 
   services:
     owncloud:
       image: owncloud/server:${OWNCLOUD_VERSION}
       restart: always
       ports:
         - ${HTTP_PORT}:8080
       depends_on:
         - db
         - redis
       environment:
         - OWNCLOUD_DOMAIN=${OWNCLOUD_DOMAIN}
         - OWNCLOUD_DB_TYPE=mysql
         - OWNCLOUD_DB_NAME=owncloud
         - OWNCLOUD_DB_USERNAME=owncloud
         - OWNCLOUD_DB_PASSWORD=owncloud
         - OWNCLOUD_DB_HOST=db
         - OWNCLOUD_ADMIN_USERNAME=${ADMIN_USERNAME}
         - OWNCLOUD_ADMIN_PASSWORD=${ADMIN_PASSWORD}
         - OWNCLOUD_MYSQL_UTF8MB4=true
         - OWNCLOUD_REDIS_ENABLED=true
         - OWNCLOUD_REDIS_HOST=redis
       healthcheck:
         test: ["CMD", "/usr/bin/healthcheck"]
         interval: 30s
         timeout: 10s
         retries: 5
       volumes:
         - /mnt/storage/owncloud-server-storage:/mnt/data
 
     db:
       image: webhippie/mariadb:latest
       restart: always
       environment:
         - MARIADB_ROOT_PASSWORD=owncloud
         - MARIADB_USERNAME=owncloud
         - MARIADB_PASSWORD=owncloud
         - MARIADB_DATABASE=owncloud
         - MARIADB_MAX_ALLOWED_PACKET=128M
         - MARIADB_INNODB_LOG_FILE_SIZE=64M
       healthcheck:
         test: ["CMD", "/usr/bin/healthcheck"]
         interval: 30s
         timeout: 10s
         retries: 5
       volumes:
         - mysql:/var/lib/mysql
         - /mnt/storage/backups/oc-backupdir/db:/var/lib/backup
 
     redis:
       image: webhippie/redis:latest
       restart: always
       environment:
         - REDIS_DATABASES=1
       healthcheck:
         test: ["CMD", "/usr/bin/healthcheck"]
         interval: 30s
         timeout: 10s
         retries: 5
       volumes:
         - redis:/var/lib/redis
   ```
4. Create a **.env** configuration file and fill it:
   ```
   cat << EOF > .env
   OWNCLOUD_VERSION=latest
   OWNCLOUD_DOMAIN=cloud.robolab.innopolis.university
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=admin
   HTTP_PORT=8088
   ```

5. Create directories for config and backup files:
`$ mkdir -p /mnt/storage/owncloud-server-storage /mnt/storage/backups/oc-backupdir/db`

6. Start the container:
`$ docker-compose up -d`

7. Check that all the containers have successfully started:
   ```
   $ docker-compose ps
                Name                           Command                 State               Ports         
   ------------------------------------------------------------------------------------------------------
   owncloud-docker-server_db_1      /usr/bin/entrypoint /bin/s      Up (healthy)   3306/tcp                                                                                
                                    ...
   owncloud-docker-                 /usr/bin/entrypoint /usr/b      Up (healthy)   0.0.0.0:8088->8080/tcp
   server_owncloud_1                ...                                                               
   owncloud-docker-server_redis_1   /usr/bin/entrypoint /bin/s      Up (healthy)   6379/tcp
                                    ...
   ```
8. Inspect the log output:
`$ docker-compose logs --follow owncloud` 

9. Wait until the output shows **"Starting apache daemon…​"**
10. To close log window press **CTRL-C**.

## Setup **config.php** parameters for proxy to work properly
1. Go to the docker directory where **docker-compose.yml** and **.env** file exists. 

2. Put ownCloud into maintenance mode:
    ```
    $ docker-compose exec owncloud occ maintenance:mode --on
    Maintenance mode enabled
    Please also consider to stop the web server on all ownCloud instances
    ```

3. Open the ownCloud **config.php** file:
`$ sudo vim /mnt/storage/owncloud-server-storage/config/config.php`

4. Add the following parameter:
`'overwritehost' => 'cloud.robolab.innopolis.university',`

5. Save changes in **config.php**.

6. Turn off maintenance mode:
`$ docker-compose exec owncloud occ maintenance:mode --off`

# Logging in

To log in to the ownCloud UI, open https://cloud.robolab.innopolis.university in your browser of choice, where you see the standard ownCloud login screen, as in the image below.

![owncloud_login_page.png](images/owncloud_login_page.png)

The username and password are the admin username and password which you stored in **.env** earlier.

**Note.** Change admin password through Web UI.

# Backup
When you backup your ownCloud server, there are four things that you need to copy:

1. Your **config/** directory.

2. Your **data/** directory.

3. Your **ownCloud database**.

## Backing Up the **config/** and **data/** directories

`$ sudo rsync -PAavxt /mnt/storage/owncloud-server-storage/config /mnt/storage/owncloud-server-storage/files /mnt/storage/backups/oc-backupdir/`

## Backup Database
Go to the docker directory where **docker-compose.yml** and **.env** file exists and launch:
`$ docker-compose exec db backup`

# OwnCloud Migration

## Assumptions
- You’re using different Docker images
  - The current Docker image (depricated) is: **owncloud**
  - The new Docker image is: **owncloud/server**
- You’re using different folders
  - The current folder is: **/mnt/storage/own-cloud/data**
  - The new folder is:  **/mnt/storage/owncloud-server-storage/files**
- You’re using different databases
  - The current database is: **owncloud_db**
  - The new database is: **owncloud**
- Database backup directory is: **/mnt/storage/backups/oc-backupdir/db**

## Description of Steps
1. Enable maintenance mode for your old and new ownCloud server
1. Sync the files from the current to the new directory
1. Migrate ownCloud database from the current to the new databse 
1. Change the ownCloud configuration to point to the new data directory
1. Disable maintenance mode for your old and new ownCloud server


### 1. Enable maintenance mode for your old and new ownCloud server
```
$ docker-compose exec owncloud occ maintenance:mode --on
Maintenance mode enabled
Please also consider to stop the web server on all ownCloud instances
```

### 2. Sync the files from the current to the new directory
Look at each section below for a detailed description.
`$ sudo rsync -PAavxt /mnt/storage/own-cloud/data/ /mnt/storage/owncloud-server-storage/files/`

### 3. Migrate ownCloud database from the current to the new databse 
* Current database
  Go to the docker directory where **.yml** file for the current ownCloud server exists and launch:
  ```
  $ docker-compose -f stack.yml exec mysql bash
  # mysqldump --single-transaction -h localhost -u root -p owncloud_db > owncloud-db-backup_`date +"%Y%m%d"`.bak
    Password: <type password>
  # exit
  $ docker cp own-cloud_mysql_1:/owncloud-db-backup_20200602.bak /mnt/storage/backups/oc-backupdir/db/
  ```
* New database
  Go to the docker directory where **.yml** file for the new ownCloud server exists and launch:
  ```
  $ docker-compose exec db bash
  # mysql -u owncloud -p owncloud < /var/lib/backup/owncloud-db-backup_20200602.bak 
    Enter password:
  ```
  Don't exit the db Docker container. It is required for the next step.

### 4. Change the ownCloud configuration to point to the new data directory
Log into mysql
  ```
   # mysql -u owncloud -p owncloud
   Enter password: 
  ```
* Update the oc_storages Table
  `DELETE FROM oc_storages WHERE id='local::/var/www/html/data/';`

* Update the oc_accounts Table
  `UPDATE oc_accounts SET home='/mnt/data/files/admin' WHERE user_id='admin';`
  `UPDATE oc_accounts SET home='/mnt/data/files/storage' WHERE user_id='storage';`
### 5. Disable maintenance mode for your old and new ownCloud server
```
$ docker-compose exec owncloud occ maintenance:mode --off
Maintenance mode disabled
```
