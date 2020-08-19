#!/bin/bash
echo "Vadetis Installation: START"

## PRE INSTALL
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
sudo \cp -r build $project_directory
sudo \cp -r run $project_directory
sudo \cp -r static $project_directory
sudo \cp -r templates $project_directory
sudo \cp -r vadetis $project_directory
sudo \cp -r vadetisweb $project_directory
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

# APACHE VHOST
echo "Create VHOST Config"
sed -e "s|\${server_name}|$server_name|" -e "s|\${server_admin}|$server_admin|" -e "s|\${project_directory}|$project_directory|" -e "s/\${project_name}/$project_name/" -e "s|\${venv_dir}|$venv_dir|" ./misc/apache_tpl/apache2_vhost.sample.conf | sudo tee /etc/apache2/sites-available/$project_name.conf

# SETUP DJANGO
echo "Install Django"
virtualenv -q -p /usr/bin/python3.7 $venv_dir
source $venv_dir/bin/activate
python3 $project_directory/manage.py makemigrations --settings vadetis.settings.production
python3 $project_directory/manage.py migrate --settings vadetis.settings.production
echo "Create Django Admin User"
python3 $project_directory/manage.py createsuperuser --settings vadetis.settings.production
python3 $project_directory/manage.py collectstatic --settings vadetis.settings.production
deactivate

# ENABLE APACHE EXTENSIONS
if ! grep -q "export LANG" "/etc/apache2/envvars"; then
  sudo echo "export LANG='en_US.UTF-8'" | sudo tee -a /etc/apache2/envvars
fi
if ! grep -q "export LC_ALL" "/etc/apache2/envvars"; then
  sudo echo "export LC_ALL='en_US.UTF-8'" | sudo tee -a /etc/apache2/envvars
fi
sudo a2enmod mod_wsgi
sudo a2ensite $project_name
sudo service apache2 reload
sudo service apache2 restart

echo "Vadetis Installation: DONE"