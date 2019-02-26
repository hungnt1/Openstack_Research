
  


## Cấu hình môi trường node controlller

  

## 1. Openstack Package 
  
- Qúa trình cài đặt sử dụng tài liệu tại : https://docs.openstack.org/rocky/install/

  
- Cài đặt Openstack Rocky Repository
```
yum install -y centos-release-openstack-rocky
```


- Upgrade hệ thống
```
yum -y upgrade
```
  
- Cài đặt OpenstackPython Client

```
yum install -y python-openstackclient
```




## 2. HAproxy

  
- Cài đặt HAproxy

```
yum install haproxy -y
```


- Khởi tạo file cấu hình ban đầu cho HAProxy
```
cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.orig

cat <<EOF > /etc/haproxy/haproxy.cfg

global
  chroot  /var/lib/haproxy
  daemon
  group  haproxy
  maxconn  4000
  pidfile  /var/run/haproxy.pid
  user  haproxy

defaults
  log  global
  maxconn  4000
  option  redispatch
  retries  3
  mode    http
  timeout  http-request 10s
  timeout  queue 1m
  timeout  connect 10s
  timeout  client 1m
  timeout  server 1m
  timeout  check 10s
  
listen stats 192.168.50.140:9000
        mode http
        stats enable
        stats uri /stats
        stats realm HAProxy\ Statistics
        stats auth admin:123@123Aa
        stats admin if TRUE

EOF
```


- Cấu hình FirewallD - stat webpage
```
firewall-cmd --add-port=9000/tcp --permanent 
firewall-cmd --reload
```

## 3. Pacemaker


**Sử dụng Pacemaker quản lý VirtualIP và HAproxy Service**


### 3.1 Cài đặt và cấu hình các thành phần

- Cài đặt Pacemaker
```
yum install -y pacemaker pcs resource-agents
```

- Khởi động dịch vụ
```
systemctl start pcsd.service
systemctl enable pcsd.service
```

- Cấu hình FirewallD

```
firewall-cmd --add-service=high-availability --permanent

firewall-cmd --reload
```

- Cấu hình mật khẩu cho tài khoản `hacluster`. Trên các node có thể sử dụng mật khẩu khác nhau

```
echo "hacluster:123@123Aa" | chpasswd
```  

- Disable chức năng stonith
```
pcs property set stonith-enabled=false --force
pcs quorum expected-votes 1

```

### 3.2 Khởi động Cluster

- Gửi request đến các node và đăng nhập

```
pcs cluster auth controller1 controller2 controller3 -u hacluster -p 123@123Aa
```  

- Boostrap Cluster
```
pcs cluster setup --force --name ops_ctl_cluster controller1 controller2 controller3
```

- Khởi động Cluster
```
pcs cluster start --all
pcs cluster enable --all
```

- Khởi tạo Resource VirtualIP ( 192.168.50.140  ) 
```
pcs resource create VirtualIP ocf:heartbeat:IPaddr2 ip=192.168.50.140 \
cidr_netmask=32 op monitor interval=2s
```

- Khởi tạo Resource HAproxy
```
pcs resource create HAproxy systemd:haproxy op monitor interval=2s
```

- Cấu hình bắt buộc HAproxy và VIP hoạt động trên cùng 1 node
```
pcs constraint order VirtualIP vip then HAproxy
pcs constraint colocation add VirtualIP with HAproxy INFINITY
```

  
## 4. Network Time Protocol ( NTP )  


### 4.1 Cài đặt và cấu hình NTP Server

- Cài đặt Chrony

```
yum install -y chrony
```

- Cấu hình NTP Server - Cho phép subnet 192.168.50.0/24 đồng bộ 
```
sed -i "s/server.*/server 0.asia.pool.ntp.org iburst/g" /etc/chrony.conf > /dev/nul
echo "allow 192.168.50.0/24" >> /etc/chrony.conf
systemctl enable chronyd.service
systemctl start chronyd.service
```

- Cấu hình FirewallD
```
firewall-cmd --add-service=ntp --permanent
firewall-cmd --reload
```

## 5. Galera MariaDB Cluster

### 5.1 Cài đặt các thành  phần 
  
- Cài đặt MariaDB và Galera
```
yum install -y mariadb mariadb-server python2-PyMySQL galera mariadb-server-galera.x86_64
```

### 5.2 .  Cấu hình Galera trên node Controlller 1

  
- Cấu hình MarriaDB Server cho OPS

```
cat <<EOF > /etc/my.cnf.d/openstack.cnf

[mysqld]
bind-address = 192.168.50.131
default-storage-engine = innodb
innodb_file_per_table = on
max_connections = 4096
collation-server = utf8_general_ci
character-set-server = utf8
EOF
```

- Khởi tạo file cấu hình tại `/etc/my.cnf.d`
```
cat <<EOF > /etc/my.cnf.d/galera.cnf
[galera]
# Mandatory settings
wsrep_on=ON
wsrep_provider=/usr/lib64/galera/libgalera_smm.so

#add your node ips here
wsrep_cluster_address="gcomm://192.168.50.131,192.168.50.132,192.168.50.133"

binlog_format=row
default_storage_engine=InnoDB
innodb_autoinc_lock_mode=2

#Cluster name
wsrep_cluster_name="galera_cluster"

# Allow server to accept connections on mgmt interfaces.
bind-address=192.168.50.131

# this server ip, change for each server
wsrep_node_address="192.168.50.131"

# this server name, change for each server
wsrep_node_name="controller1"

wsrep_sst_method=rsync

EOF

```


- Cấu hình FirewallD
```
firewall-cmd --add-port={3306/tcp,4567/tcp,4568/tcp,4444/tcp} --permanent
firewall-cmd --reload
```

- Tạm dừng dịch vụ
```
systemctl stop mariadb
```


### 5.2.  Cấu hình Galera trên node Controlller 2 
  
- Cấu hình MarriaDB Server cho OPS

```
cat <<EOF > /etc/my.cnf.d/openstack.cnf
[mysqld]
bind-address = 192.168.50.132
default-storage-engine = innodb
innodb_file_per_table = on
max_connections = 4096
collation-server = utf8_general_ci
character-set-server = utf8
EOF
```


- Khởi tạo file cấu hình tại `/etc/my.cnf.d`
```
cat <<EOF > /etc/my.cnf.d/openstack.cnf

[mysqld]
bind-address = 192.168.50.133
default-storage-engine = innodb
innodb_file_per_table = on
max_connections = 4096
collation-server = utf8_general_ci
character-set-server = utf8
EOF
```


- Khởi tạo file cấu hình tại `/etc/my.cnf.d`
```
cat <<EOF > /etc/my.cnf.d/galera.cnf
[galera]
# Mandatory settings
wsrep_on=ON
wsrep_provider=/usr/lib64/galera/libgalera_smm.so

#add your node ips here
wsrep_cluster_address="gcomm://192.168.50.131,192.168.50.132,192.168.50.133"

binlog_format=row
default_storage_engine=InnoDB
innodb_autoinc_lock_mode=2

#Cluster name
wsrep_cluster_name="galera_cluster"

# Allow server to accept connections on mgmt interfaces.
bind-address=192.168.50.132

# this server ip, change for each server
wsrep_node_address="192.168.50.132"

# this server name, change for each server
wsrep_node_name="controller2"

wsrep_sst_method=rsync

EOF

```


- Cấu hình FirewallD
```
firewall-cmd --add-port={3306/tcp,4567/tcp,4568/tcp,4444/tcp} --permanent
firewall-cmd --reload
```


### 5.3.  Cấu hình Galera trên node Controlller 3  ( Boostrap Cluster ) 
  
- Cấu hình MarriaDB Server cho OPS
```
cat <<EOF > /etc/my.cnf.d/openstack.cnf

[mysqld]
bind-address = 192.168.50.133
default-storage-engine = innodb
innodb_file_per_table = on
max_connections = 4096
collation-server = utf8_general_ci
character-set-server = utf8
EOF
```


- Khởi tạo file cấu hình tại `/etc/my.cnf.d`
```
cat <<EOF > /etc/my.cnf.d/galera.cnf
[galera]
# Mandatory settings
wsrep_on=ON
wsrep_provider=/usr/lib64/galera/libgalera_smm.so

#add your node ips here
wsrep_cluster_address="gcomm://192.168.50.131,192.168.50.132,192.168.50.133"

binlog_format=row
default_storage_engine=InnoDB
innodb_autoinc_lock_mode=2

#Cluster name
wsrep_cluster_name="galera_cluster"

# Allow server to accept connections on mgmt interfaces.
bind-address=192.168.50.133

# this server ip, change for each server
wsrep_node_address="192.168.50.133"

# this server name, change for each server
wsrep_node_name="controller3"

wsrep_sst_method=rsync

EOF

```


- Cấu hình FirewallD
```
firewall-cmd --add-port={3306/tcp,4567/tcp,4568/tcp,4444/tcp} --permanent
firewall-cmd --reload
```

 -   Khởi tạo Cluster
```
galera_new_cluster
```

- Khởi tạo Password User root ( tùy chọn )
```
mysqladmin --user=root password "123@123Aa"
```


### 5.4. Khởi động dịch vụ

- Khởi động dịch vụ

```
systemctl start mariadb
systemctl enable mariadb
```




## 6. RabbitMQ

### 6.1. Cài đặt RabbitMQ Server

- Cài đặt package
```
yum -y install rabbitmq-server

```

-   Khởi động Web Management Interface , xòa tài khoản guest, khởi động tài khoản mới
```
rabbitmq-plugins enable rabbitmq_management
systemctl restart rabbitmq-server
rabbitmqctl delete_user guest
rabbitmqctl add_user nguyenhungsync 123@123Aa 
rabbitmqctl set_user_tags nguyenhungsync administrator 
rabbitmqctl add_user openstack rabbitmq_123
rabbitmqctl set_permissions openstack ".*" ".*" ".*"

```

-   Cấu hình FirewallD Rule
```
firewall-cmd --add-port=15672/tcp --permanent   ## Web Interface
firewall-cmd --add-port=5672/tcp --permanent  ## RabitMQ Server
firewall-cmd --add-port={4369/tcp,25672/tcp} --permanent ## RabitMQ Cluster Port
firewall-cmd --reload
```

- Cấu hình HA policy 
```
rabbitmqctl set_policy ha-all '^(?!amq\.).*' '{"ha-mode": "all"}'
```

### 6.2. Khởi động Cluster

- Copy Erlang cookie từ controller node 1 sang các node khác 
```
scp /var/lib/rabbitmq/.erlang.cookie root@controller2:/var/lib/rabbitmq/
scp /var/lib/rabbitmq/.erlang.cookie root@controller3:/var/lib/rabbitmq/
rabbitmqctl start_app
```

- Khởi động dịch vụ trên tất cả các node  
```
systemctl enable rabbitmq-server.service
systemctl start rabbitmq-server.service
```


- Thực hiện join vào cluster từ các node khác controller1
```
rabbitmqctl stop_app
rabbitmqctl join_cluster rabbit@controller1  ## phải sử dụng hostname
rabbitmqctl start_app

```


- Kiểm tra Cluster
```
rabbitmqctl cluster_status
```

### 6.3. Cấu hình OpenStack Service sử dụng RabbitMQ HA

- Cấu hình các node
```
rabbit_hosts=controlller1:5672,controller2:5672,controller3:5672
```

- Cấu hình thời gian thử lại kết nối tới RabbitMQ Server
```
rabbit_retry_interval=1
```

- Số lần cố gắn kết nối tới RabbitMQ trước khi đưa về trạng thái down
```
rabbit_retry_backoff=2
```

- Sử dụng HA queue 
```
rabbit_ha_queues=true
```

- Lưu lại hàng đợi khi broker restart

```
rabbit_durable_queues=true
```



## 7. Memcached

### 7.1 Cài đặt và cấu hình Memcached
```
 yum install -y memcached python-memcached
```


- Cho phép truy cập qua địa chỉ IP Management ( địa chỉ trên của các node ) 
```
sed -i "s/-l 127.0.0.1,::1/-l 127.0.0.1,::1,$IP_NODE/g" /etc/sysconfig/memcached
```

- Cấu hình FirewallD
```
firewall-cmd --add-port=11211/tcp --permanent
firewall-cmd --reload
```


- Khởi động dịch vụ
```
systemctl enable memcached.service
systemctl start memcached.service
```


#### 7.2. Khai báo HA

- Cấu trúc khai báo  
```
Memcached_servers = controller1:11211,controller2:11211,controller3:11211
```




## 8 Cấu hình HAproxy 

### 8.1. Cấu hình HAproxy và Pacemaker cho cụm MariaDB


-  Clustercheck là  chương trình bash hữu ích để tạo proxy (ví dụ: HAProxy) có khả năng giám sát Galera MariaDB Cluster
-  Cấu hình Clustercheck
```
# Get bash program , socket and server 
wget https://raw.githubusercontent.com/nguyenhungsync/percona-clustercheck/master/clustercheck -P /usr/bin
wget https://raw.githubusercontent.com/nguyenhungsync/percona-clustercheck/master/systemd/mysqlchk.sockeariaDBt -P /usr/lib/systemd/system
wget https://raw.githubusercontent.com/nguyenhungsync/percona-clustercheck/master/systemd/mysqlchk%40.service -P /usr/lib/systemd/system

## Phan quyen 
chmod +x /usr/bin/clustercheck
chmod +r /usr/lib/systemd/system/mysqlchk.socket
chmod +r /usr/lib/systemd/system/mysqlchk@.service

## Khoi tao user check

mysql -u root -e "GRANT PROCESS ON *.* TO 'clustercheckuser'@'localhost' IDENTIFIED BY '123@123Aa'"

## Start socket

systemctl enable mysqlchk.socket
systemctl start mysqlchk.socket

## FirewallD

firewall-cmd --add-port=9200/tcp --permanent
firewall-cmd --reload

```

- Cấu hình HAproxy cho dịch vụ MariaDB tại `/etc/haproxy/haproxy.cfg`
```
cat <<EOF >>  /etc/haproxy/haproxy.cfg
listen mariadb_cluster 192.168.50.140:3306
        mode tcp
        balance leastconn
        option httpchk
        default-server port 9200 inter 2s downinter 5s rise 3 fall 2 slowstart 60s maxconn 64 maxqueue 128 weight 100
        server mariadb1 192.168.50.131:3306 check 
        server mariadb2 192.168.50.132:3306 check backup
        server mariadb3 192.168.50.133:3306 check backup 
EOF
```

- Khởi động lại Resource HAproxy

```
pcs resource restart HAproxy
```

- Chuyển Resource về Node Controlller 1 ( để node 1 làm master cho các cấu hình Service)

```
pcs resource move VirtualIP controller1

```

END.