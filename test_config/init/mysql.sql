DROP DATABASE IF EXISTS `hsmaster`;
CREATE DATABASE IF NOT EXISTS `hsmaster`;
DROP DATABASE IF EXISTS `db`;
CREATE DATABASE IF NOT EXISTS `db`;

GRANT ALL ON `hsmaster`.* TO 'mysql'@'%';
GRANT ALL ON `db`.* TO 'mysql'@'%';