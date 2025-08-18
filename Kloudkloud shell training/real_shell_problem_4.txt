Day by day traffic is increasing on one of the websites managed by the Nautilus production support team. Therefore, the team has observed a degradation in website performance. Following discussions about this issue, the team has decided to deploy this application on a high availability stack i.e on Nautilus infra in Stratos DC. They started the migration last month and it is almost done, as only the LBR server configuration is pending. Configure LBR server as per the information given below:


a. Install nginx on LBR (load balancer) server.


b. Configure load-balancing with the an http context making use of all App Servers. Ensure that you update only the main Nginx configuration file located at /etc/nginx/nginx.conf.


c. Make sure you do not update the apache port that is already defined in the apache configuration on all app servers, also make sure apache service is up and running on all app servers.


d. Once done, you can access the website using StaticApp button on the top bar.


-------------------- SOLUTION --------------------
||||||||||||||||||||||||||||||||||||||||||||||||||

Edit the main Nginx config file
File: /etc/nginx/nginx.conf

Find the existing http { ... } block and modify it like this (don’t touch other global configs):

http {
    upstream app_servers {
        server stapp01:8080;   # Replace with App Server hostnames/IPs + apache port
        server stapp02:8080;
        server stapp03:8080;
    }

    server {
        listen 80;

        location / {
            proxy_pass http://app_servers;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
}


🔹 Here:

stapp01, stapp02, stapp03 are the App Server hostnames (use /etc/hosts entries if needed).

Port 8080 (or whichever Apache is listening on) must be used.

We do not change Apache ports on App servers, only point Nginx to them.

Check Nginx config syntax

sudo nginx -t


Restart and enable Nginx

sudo systemctl restart nginx
sudo systemctl enable nginx