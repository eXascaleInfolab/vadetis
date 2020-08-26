#!/bin/bash
echo "Vadetis Installation: START"

# PRE INSTALL
sudo apt update

# MySQL
sudo apt install mysql-server libmysqlclient-dev
# Run the MySQL Secure Installation wizard, utility prompts you to define the mysql root password and other security-related options
sudo mysql_secure_installation utility
sudo systemctl start mysql
sudo systemctl enable mysql

# CONFIGURATION
echo "Leave blank to use default values"
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

read -p "Enter database user [default: vadetisadmin]: " vadetis_db_user
vadetis_db_user=${vadetis_db_user:-vadetisadmin}
read -p "Enter database user password [default: Cast40analysts5Roofing]: " db_user_pw
db_user_pw=${db_user_pw:-Cast40analysts5Roofing}

read -p "Enter SMTP host [default: smtp.gmail.com]: " smtp_host
smtp_host=${smtp_host:-smtp.gmail.com}
read -p "Enter SMTP port [default: 587]: " smtp_port
smtp_port=${smtp_port:-587}
read -p "Enter mail user [default: lisaexascale@gmail.com]: " mail_user
mail_user=${mail_user:-lisaexascale@gmail.com}
read -p "Enter mail user password [default: svQcdxXQ]: " mail_user_pwd
mail_user_pwd=${mail_user_pwd:-svQcdxXQ}

# INSTALL DATABASE
read -s -p "Enter MySQL ROOT Password: " mysql_password
echo "Install database... "
mysql_password="$mysql_password"
echo "Drop existing schema..."
mysql -u root --password="$mysql_password" -h localhost -e "
DROP SCHEMA IF EXISTS $project_name;
"
echo "Create new schema..."
mysql -u root --password="$mysql_password" -h localhost -e "
CREATE SCHEMA $project_name DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_general_ci;
"
echo "Create mysql user..."
mysql -u root --password="$mysql_password" -h localhost -e "
CREATE USER IF NOT EXISTS $vadetis_db_user@'localhost' IDENTIFIED BY '$db_user_pw';
GRANT ALL PRIVILEGES ON $project_name.* TO $vadetis_db_user@'localhost';
FLUSH PRIVILEGES;
"
echo "Install database done"

# PYTHON
echo "Install Python 3.7"
sudo apt install python3.7 python3.7-dev python3-pip python3.7-venv

# APACHE2
echo "Install Apache2"
sudo apt install apache2 apache2-dev apache2-utils ssl-cert

# INSTALL MOD WSGI
echo "Install MOD WSGI"
wget https://github.com/GrahamDumpleton/mod_wsgi/archive/4.7.1.tar.gz
tar xvfz 4.7.1.tar.gz
sudo rm -rf 4.7.1.tar.gz
cd mod_wsgi-4.7.1/
./configure --with-python=/usr/bin/python3.7
sudo make
sudo make install
sudo echo "LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so" | sudo tee /etc/apache2/mods-available/mod_wsgi.load
cd ..
sudo rm -rf mod_wsgi-4.7.1

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

# PRODUCTIVE SETTINGS
sed -e "s|\${server_name}|$server_name|" -e "s/\${project_name}/$project_name/" -e "s|\${vadetis_db_user}|$vadetis_db_user|" -e "s|\${db_user_pw}|$db_user_pw|" -e "s|\${smtp_host}|$smtp_host|" -e "s|\${smtp_port}|$smtp_port|" -e "s|\${mail_user}|$mail_user|" -e "s|\${mail_user_pwd}|$mail_user_pwd|" ./misc/settings_tpl/production_settings_tpl.tpl | sudo tee $project_directory/vadetis/settings/production.py

# SET RIGHTS
# Adding current user to www-data
sudo adduser $USER www-data
# Change ownership to user:www-data and
sudo chown $USER:www-data -R $project_directory
sudo chmod u=rwX,g=srX,o=rX -R $project_directory
sudo chown $USER:www-data -R $venv_dir
sudo chmod u=rwX,g=srX,o=rX -R $venv_dir

# change file permissions of existing files and folders to 755/644
sudo find $project_directory -type d -exec chmod g=rwxs "{}" \;
sudo find $project_directory -type f -exec chmod g=rws "{}" \;
sudo find $venv_dir -type d -exec chmod g=rwxs "{}" \;
sudo find $venv_dir -type f -exec chmod g=rws "{}" \;

# INSTALL PYTHON REQUIREMENTS
echo "Install Python Requirements"
python3.7 -m venv $venv_dir
source $venv_dir/bin/activate
pip3 install -U wheel --user
pip3 install -r requirements.txt
deactivate

# APACHE VHOST
echo "Create VHOST Config"
sed -e "s|\${server_name}|$server_name|" -e "s|\${server_admin}|$server_admin|" -e "s|\${project_directory}|$project_directory|" -e "s/\${project_name}/$project_name/" -e "s|\${venv_dir}|$venv_dir|" ./misc/apache_tpl/apache2_vhost.sample.conf | sudo tee /etc/apache2/sites-available/$project_name.conf

# SETUP DJANGO
echo "Install Django"
source $venv_dir/bin/activate
python3 $project_directory/manage.py makemigrations --settings vadetis.settings.production
python3 $project_directory/manage.py migrate --settings vadetis.settings.production
echo "Create Django Admin User..."
python3 $project_directory/manage.py createsuperuser --settings vadetis.settings.production
python3 $project_directory/manage.py collectstatic --settings vadetis.settings.production
deactivate

# ENABLE APACHE EXTENSIONS
if ! grep -q "export LANG='en_US.UTF-8'" "/etc/apache2/envvars"; then
  sudo echo "export LANG='en_US.UTF-8'" | sudo tee -a /etc/apache2/envvars
fi
if ! grep -q "export LC_ALL" "/etc/apache2/envvars"; then
  sudo echo "export LC_ALL='en_US.UTF-8'" | sudo tee -a /etc/apache2/envvars
fi

# ACTIVATE ALL DJANGO USERS and SET DJANGO SITE
mysql -u root --password="$mysql_password" -h localhost -e "
INSERT INTO $project_name.account_emailaddress (email, verified, \`primary\`, user_id) SELECT u.email, 1, 0, u.id FROM $project_name.auth_user u WHERE u.is_superuser = 1;
DELETE FROM $project_name.django_site;
INSERT INTO $project_name.django_site (id, domain, name) VALUES (1, '$server_name', 'Vadetis');
"

# etc/hosts
if ! grep -q "127.0.0.1  $server_name" "/etc/hosts"; then
  sudo echo "$server_name not in /etc/hosts, will append.."
  sudo echo "127.0.0.1  $server_name" | sudo tee -a /etc/hosts
fi

# CONFIGURE AND START APACHE
sudo a2enmod mod_wsgi
sudo a2dissite 000-default
sudo a2ensite $project_name
sudo service apache2 reload
sudo service apache2 restart

echo "Vadetis Installation: DONE"
echo "You may have to check your /etc/hosts file according to your network configuration."
echo "Check the production.py settings file in the deployment folder for additional security settings."
