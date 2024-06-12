CREATE USER maxscale@'%' IDENTIFIED BY 'mariadb'; 

GRANT ALL PRIVILEGES ON *.* TO maxscale@'%';

CREATE DATABASE `keycloak-database`;