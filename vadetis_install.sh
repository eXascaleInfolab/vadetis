#!/bin/bash
echo "Vadetis Installation: START"

# PRE INSTALL
sudo apt update

# MySQL
sudo apt install mysql-server
# Run the MySQL Secure Installation wizard, utility prompts you to define the mysql root password and other security-related options
sudo mysql_secure_installation utility
sudo systemctl start mysql
sudo systemctl enable mysql

# INSTALL DATABASE
read -s -p "Enter MySQL Root Password: " mysql_password
echo "Install database... "
mysql_password="$mysql_password"
echo "Drop existing schema..."
mysql -u root --password="$mysql_password" -h localhost -e '
DROP SCHEMA IF EXISTS vadetisv2;
'
echo "Create new schema..."
mysql -u root --password="$mysql_password" -h localhost -e '
CREATE SCHEMA vadetisv2 DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_general_ci;
'
echo "Create mysql user..."
mysql -u root --password="$mysql_password" -h localhost -e "
CREATE USER IF NOT EXISTS 'vadetisadmin'@'localhost' IDENTIFIED BY 'Cast40analysts5Roofing';
GRANT ALL PRIVILEGES ON vadetisv2.* TO 'vadetisadmin'@'localhost';
FLUSH PRIVILEGES;
"
echo "Install database done"

# PYTHON
echo "Install Python 3.7"
sudo apt install python3.7 python3-pip python3.7-venv

# APACHE2
echo "Install Apache2"
sudo apt install apache2 apache2-dev apache2-utils ssl-cert libapache2-mod-wsgi

# CONFIGURATION
read -p "Enter domain [default: vadetis.exascale.info]: " server_name
server_name=${server_name:-vadetis.exascale.info}
read -p "Enter server admin [default: webmaster@vadetis.exascale.info]: " server_admin
server_admin=${server_admin:-webmaster@vadetis.exascale.info}
read -p "Enter project directory [default: /var/www/vadetis.exascale.info]: " project_directory
project_directory=${project_directory:-/var/www/vadetis.exascale.info}
sudo mkdir -p $project_directory
read -p "Enter project name [default: vadetis]: " project_name
project_name=${project_name:-vadetis}
read -p "Enter venv directory [default: /usr/local/venvs/venv_vadetis]: " venv_dir
venv_dir=${venv_dir:-/usr/local/venvs/venv_vadetis}
sudo mkdir -p $venv_dir

# COPY CONTENTS
echo "Copy files"
sudo \cp build $project_directory
sudo \cp run $project_directory
sudo \cp static $project_directory
sudo \cp templates $project_directory
sudo \cp vadetis $project_directory
sudo \cp vadetisweb $project_directory
sudo \cp *.py $project_directory
sudo \cp requirements.txt $project_directory
sudo \cp README.md $project_directory

# SET RIGHTS
# Adding current user to www-data
sudo adduser $USER www-data
# change ownership to user:www-data and
sudo chown $USER:www-data -R $project_directory
sudo chmod u=rwX,g=srX,o=rX -R $project_directory

# change file permissions of existing files and folders to 755/644
sudo find $project_directory -type d -exec chmod g=rwxs "{}" \;
sudo find $project_directory -type f -exec chmod g=rws "{}" \;

# INSTALL PYTHON REQUIREMENTS
echo "Install Python Requirements"
virtualenv -q -p /usr/bin/python3.7 $venv_dir
source $venv_dir/bin/activate
pip3 install -r requirements.txt
deactivate

# ENABLE APACHE EXTENSION


# SETUP DJANGO


echo "Vadetis Installation: DONE"