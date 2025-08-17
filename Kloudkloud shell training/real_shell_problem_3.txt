The system admins team of xFusionCorp Industries needs to deploy a new application on App Server 3 in Stratos Datacenter. They have some pre-requites to get ready that server for application deployment. Prepare the server as per requirements shared below:


1. Install and configure nginx on App Server 3.


2. On App Server 3 there is a self signed SSL certificate and key present at location /tmp/nautilus.crt and /tmp/nautilus.key. Move them to some appropriate location and deploy the same in Nginx.


3. Create an index.html file with content Welcome! under Nginx document root.


4. For final testing try to access the App Server 3 link (either hostname or IP) from jump host using curl command. For example curl -Ik https://<app-server-ip>/.

-------------------- SOLUTION --------------------
||||||||||||||||||||||||||||||||||||||||||||||||||

1) Install and start Nginx (App Server 3)

Why: We need a running web server before we can serve HTTPS.

# Install nginx
sudo yum install -y nginx                # (Ubuntu/Debian: sudo apt update && sudo apt install -y nginx)

# Enable and start on boot
sudo systemctl enable nginx
sudo systemctl start nginx

# Check it actually started
sudo systemctl status nginx --no-pager


Verify listening ports:

sudo ss -tulnp | grep nginx             # expect to see :80 (HTTP) now


Default document root on CentOS/RHEL is /usr/share/nginx/html.

If a firewall is enabled, allow HTTP/HTTPS (we’ll use HTTPS shortly):

sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

2) Move the self-signed cert/key and configure HTTPS

Why: Cert/key should live in a secure, conventional path. Nginx must be told where they are and to listen on 443.

# Create a secure directory for TLS material
sudo mkdir -p /etc/nginx/ssl

# Move the provided files from /tmp to nginx's ssl dir
sudo mv /tmp/key.crt /etc/nginx/ssl/
sudo mv /tmp/key.key /etc/nginx/ssl/

# Lock down permissions (key should not be world-readable)
sudo chown root:root /etc/nginx/ssl/key.crt /etc/nginx/ssl/key.key
sudo chmod 644 /etc/nginx/ssl/key.crt
sudo chmod 600 /etc/nginx/ssl/key.key

# If SELinux is enforcing, fix contexts so nginx can read them
sudo restorecon -Rv /etc/nginx/ssl


Create an HTTPS server block:

# Create a dedicated nginx vhost config
sudo tee /etc/nginx/conf.d/ssl_site.conf > /dev/null <<'CONF'
server {
    listen 443 ssl;                      # standard HTTPS port
    server_name _;                       # use _ for any hostname (or replace with stapp03 / server FQDN)

    root /usr/share/nginx/html;          # document root
    index index.html;

    ssl_certificate     /etc/nginx/ssl/key.crt;
    ssl_certificate_key /etc/nginx/ssl/key.key;

    # (Optional) Basic TLS settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
}

# (Optional) redirect HTTP -> HTTPS
server {
    listen 80;
    server_name _;
    return 301 https://$host$request_uri;
}
CONF


Validate config and reload:

sudo nginx -t                              # must show: syntax is ok / test is successful
sudo systemctl reload nginx


Verify HTTPS is listening:

sudo ss -tulnp | grep ':443'               # should show nginx on 0.0.0.0:443 (and/or [::]:443)

3) Create the document root page

Why: You want a visible page to confirm Nginx serves content over HTTPS.

echo 'Welcome!' | sudo tee /usr/share/nginx/html/index.html > /dev/null


(Optional) sanity check locally on the server:

curl -I http://localhost/                 # should return HTTP/1.1 301 to https if you kept the redirect
curl -Ik https://localhost/               # -I = HEAD, -k = ignore self-signed cert

4) Final test from the jump host

Why: You want to confirm reachability from outside, exactly like in the task.

# From the jump host, replace <HOSTNAME_OR_IP> with App Server 3’s hostname or IP
curl -Ik https://<HOSTNAME_OR_IP>/