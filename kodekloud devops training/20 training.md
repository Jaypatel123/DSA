The Nautilus application development team is planning to launch a new PHP-based application, which they want to deploy on Nautilus infra in Stratos DC. The development team had a meeting with the production support team and they have shared some requirements regarding the infrastructure. Below are the requirements they shared:



a. Install nginx on app server 3 , configure it to use port 8093 and its document root should be /var/www/html.


b. Install php-fpm version 8.3 on app server 3, it must use the unix socket /var/run/php-fpm/default.sock (create the parent directories if don't exist).


c. Configure php-fpm and nginx to work together.


d. Once configured correctly, you can test the website using curl http://stapp03:8093/index.php command from jump host.

NOTE: We have copied two files, index.php and info.php, under /var/www/html as part of the PHP-based application setup. Please do not modify these files.


###########################
########### Solution vvvvvvvvvvvvvvvvvvv run below commands
###########################

ssh banner@172.16.238.12

sudo yum install nginx vim -y

sudo /etc/nginx/nginx.conf

    server {

        listen 8093;
        server_name stapp03; # add either stapp03 or _ 

        root /var/www/html;
        index index.php index.html;

        location / {
            try_files $uri $uri/ =404;
        }

        location ~ \.php$ {
            include fastcgi_params;
            fastcgi_pass unix:unix:/var/run/php-fpm/default.sock;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        }
    }


sudo systemctl restart nginx
sudo systemctl enable nginx

# Install php-fpm 8.3 and Configure UNIX Socket

sudo yum install epel-release -y
sudo yum install https://rpms.remirepo.net/enterprise/remi-release-9.rpm -y
sudo yum module reset php -y
sudo yum module enable php:remi-8.3 -y
sudo yum install php php-fpm php-cli -y

sudo mkdir -p /var/run/php-fpm

sudo vim /etc/php-fpm.d/www.conf
    listen = /var/run/php-fpm/default.sock
    listen.owner = nginx
    listen.group = nginx
    listen.mode = 0660


sudo systemctl restart php-fpm
sudo systemctl enable php-fpm

sudo chown -R nginx:nginx /var/www/html


https://chatgpt.com/c/69196416-a918-832f-8539-8dcd1a40d713