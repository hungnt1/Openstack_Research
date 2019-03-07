

## Cấu hình môi trường node Compute và Storage Node


## 1. Openstack Package


- Cài đặt Openstack Rocky Repository

```
yum install -y centos-release-openstack-rocky
yum upgrade -y
```



## 2. NTP

- Cài đặt chrony

```
 yum install -y chrony
```

- Cấu hình NTP ( sử dụng Pacemaker VIP)

```
sed -i "s/server.*/server 192.168.50.140 iburst/g" /etc/chrony.conf
systemctl enable chronyd.service
systemctl restart chronyd.service
```

END. 