
  


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

- https://github.com/nguyenhungsync/Openstack_Research/blob/master/High-availability/7.%20Cluster-Openstack/Pacemaker/10.HAproxy-Service.md



- Cấu hình FirewallD - stat webpage
```
firewall-cmd --add-port=9000/tcp --permanent 
firewall-cmd --reload
```

## 3. Pacemaker


**Sử dụng Pacemaker quản lý VirtualIP và HAproxy Service**


### 3.1 Cài đặt và cấu hình các thành phần trên các node Controller

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



### 3.2 Khởi động động Cluster trên Controller 1

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
pcs constraint order VirtualIP then HAproxy
pcs constraint colocation add VirtualIP with HAproxy INFINITY
```


### 3.2 . Khởi động, chuyển resource


- Disable chức năng stonith
```
pcs property set stonith-enabled=false --force
pcs quorum expected-votes 1

```

- Disable mode quorum

```
pcs property set no-quorum-policy=ignore

```


- Chuyển Resource về Node Controlller 1 ( để node 1 làm master cho các cấu hình Service)

```
pcs resource move VirtualIP controller1

```
  
## 4. Network Time Protocol ( NTP )  


### 4.1 Cài đặt và cấu hình NTP Server

- Cài đặt Chrony

```
yum install -y chrony
```

- Cấu hình NTP Server - Cho phép subnet 192.168.50.0/24 đồng bộ 
```
sed -i "s/server.*/server vn.pool.ntp.org iburst/g" /etc/chrony.conf > /dev/nul
echo "allow 192.168.50.0/24" >> /etc/chrony.conf
systemctl enable chronyd.service
systemctl restart chronyd.service
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
log_error = /var/log/mariadb/error.log
bind-address = 192.168.50.131
default-storage-engine = innodb
innodb_file_per_table = on
max_connections = 1000
collation_server = utf8_general_ci
character_set_server = utf8
expire_logs_days = 7
log_slave_updates = 1
log_bin_trust_function_creators = 1
max_connect_errors = 1000
wait_timeout = 28800
tmp_table_size = 32M
net_read_timeout = 2000
net_write_timeout = 2000
max_heap_table_size = 32M
query_cache_type = 0
query_cache_size = 0M
thread_cache_size = 30
thread_pool_idle_timeout = 30
open_files_limit = 1024
table_definition_cache = 100M
innodb_flush_method = O_DIRECT
innodb_log_file_size = 300MB
innodb_flush_log_at_trx_commit = 1
innodb_buffer_pool_size = 1024M
innodb_buffer_pool_instances = 1
innodb_read_io_threads = 4
innodb_write_io_threads = 4
innodb_doublewrite = ON
innodb_log_buffer_size = 128M
innodb_thread_concurrency = 0
innodb_stats_on_metadata = 0
connect_timeout = 28800
max_allowed_packet = 500M
max_statement_time = 3600
skip_name_resolve


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
innodb_locks_unsafe_for_binlog=1
default_storage_engine=InnoDB
innodb_autoinc_lock_mode=2
wsrep_slave_threads=2
wsrep_convert_LOCK_to_trx=0
wsrep_retry_autocommit=1
wsrep_auto_increment_control=1

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
log_error = /var/log/mariadb/error.log
bind-address = 192.168.50.132
default-storage-engine = innodb
innodb_file_per_table = on
max_connections = 1000
collation_server = utf8_general_ci
character_set_server = utf8
expire_logs_days = 7
log_slave_updates = 1
log_bin_trust_function_creators = 1
max_connect_errors = 1000
wait_timeout = 28800
tmp_table_size = 32M
net_read_timeout = 2000
net_write_timeout = 2000
max_heap_table_size = 32M
query_cache_type = 0
query_cache_size = 0M
thread_cache_size = 30
thread_pool_idle_timeout = 30
open_files_limit = 1024
table_definition_cache = 100M
innodb_flush_method = O_DIRECT
innodb_log_file_size = 300MB
innodb_flush_log_at_trx_commit = 1
innodb_buffer_pool_size = 1024M
innodb_buffer_pool_instances = 1
innodb_read_io_threads = 4
innodb_write_io_threads = 4
innodb_doublewrite = ON
innodb_log_buffer_size = 128M
innodb_thread_concurrency = 0
innodb_stats_on_metadata = 0
connect_timeout = 28800
max_allowed_packet = 500M
max_statement_time = 3600
skip_name_resolve


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
innodb_locks_unsafe_for_binlog=1
default_storage_engine=InnoDB
innodb_autoinc_lock_mode=2
wsrep_slave_threads=2
wsrep_convert_LOCK_to_trx=0
wsrep_retry_autocommit=1
wsrep_auto_increment_control=1

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
log_error = /var/log/mariadb/error.log
bind-address = 192.168.50.133
default-storage-engine = innodb
innodb_file_per_table = on
max_connections = 1000
collation_server = utf8_general_ci
character_set_server = utf8
expire_logs_days = 7
log_slave_updates = 1
log_bin_trust_function_creators = 1
max_connect_errors = 1000
wait_timeout = 28800
tmp_table_size = 32M
net_read_timeout = 2000
net_write_timeout = 2000
max_heap_table_size = 32M
query_cache_type = 0
query_cache_size = 0M
thread_cache_size = 30
thread_pool_idle_timeout = 30
open_files_limit = 1024
table_definition_cache = 100M
innodb_flush_method = O_DIRECT
innodb_log_file_size = 300MB
innodb_flush_log_at_trx_commit = 1
innodb_buffer_pool_size = 1024M
innodb_buffer_pool_instances = 1
innodb_read_io_threads = 4
innodb_write_io_threads = 4
innodb_doublewrite = ON
innodb_log_buffer_size = 128M
innodb_thread_concurrency = 0
innodb_stats_on_metadata = 0
connect_timeout = 28800
max_allowed_packet = 500M
max_statement_time = 3600
skip_name_resolve


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
innodb_locks_unsafe_for_binlog=1
default_storage_engine=InnoDB
innodb_autoinc_lock_mode=2
wsrep_slave_threads=2
wsrep_convert_LOCK_to_trx=0
wsrep_retry_autocommit=1
wsrep_auto_increment_control=1

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

 - Khởi tạo Cluster
```
galera_new_cluster
```

- Khởi tạo Password User root ( tùy chọn )
```
mysqladmin --user=root password "123@123Aa"
```

### Hết cấu hình

### 5.4. Khởi động  động dịch vụ trên các Controller Node 

- Khởi động dịch vụ

```
systemctl start mariadb
systemctl enable mariadb
```


### 5.5. Cấu hình Cluster check trên các Controller Node


-  Clustercheck là  chương trình bash hữu ích để tạo proxy (ví dụ: HAProxy) có khả năng giám sát Galera MariaDB Cluster
-  Cấu hình Clustercheck
```
## cai dat package

yum install -y xinetd wget

# Get bash program , socket and server 
wget https://raw.githubusercontent.com/nguyenhungsync/percona-clustercheck/master/clustercheck
chmod +x clustercheck
mv clustercheck /usr/bin/


## Khoi tao user check

mysql > GRANT PROCESS ON *.* TO 'clustercheckuser'@'localhost' IDENTIFIED BY '123@123Aa'


## Khoi tao Service

cat <<EOF>  /etc/xinetd.d/mysqlchk
# default: on
# description: mysqlchk
service mysqlchk
{
        disable = no
        flags = REUSE
        socket_type = stream
        port = 9200
        wait = no
        user = nobody
        server = /usr/bin/clustercheck
        log_on_failure += USERID
        only_from = 0.0.0.0/0
        per_source = UNLIMITED
}
EOF

# Tạo service
echo 'mysqlchk 9200/tcp # MySQL check' >> /etc/services


# Bật xinetd
systemctl restart xinetd
systemctl enable xinetd

## FirewallD

firewall-cmd --add-port={9200/tcp,4444/tcp} --permanent
firewall-cmd --reload

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

- Cấu hình HA policy 
```
rabbitmqctl set_policy ha-all '^(?!amq\.).*' '{"ha-mode": "all"}'
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


END.
