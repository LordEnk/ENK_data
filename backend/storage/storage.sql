-- script to create a user ENK and database enkdata grnting all privilages
CREATE DATABASE enk_data;

CREATE USER 'ENK'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON enk_data.* TO 'yourusername'@'localhost';
FLUSH PRIVILEGES;

