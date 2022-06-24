
## Cấu hình không cho phép cloud-init tự động cấu hình network
- Bình thường cloud-init sẽ tự động khởi tạo các file cấu hình ifupdown trên máy VM Centos 7.x, việc này có thể gây một số cản trờ trong quá trình VM sử dụng
```
[root@centos-c ~]# cat /etc/sysconfig/network-scripts/ifcfg-eth0
# Created by cloud-init on instance boot automatically, do not edit.
#
BOOTPROTO=dhcp
DEVICE=eth0
HWADDR=fa:16:3e:47:c9:64
ONBOOT=yes
TYPE=Ethernet
USERCTL=no

```

- Để ngăn chặn việc cloud-init tự động khởi tạo file cấu hình, khi đóng template cho openstack cần cấu hình thêm 
```
echo "network: {config: disabled}" | sudo tee /etc/cloud/cloud.cfg.d/99-disable-network-config.cfg
```
- Và tạo thêm file cấu hình cho eth0 ( cái này tùy vào driver, virtio thì sẽ là eth0) trong template như sau

```
[root@centos-c ~]# cat /etc/sysconfig/network-scripts/ifcfg-eth0
BOOTPROTO=dhcp
DEVICE=eth0
ONBOOT=yes
TYPE=Ethernet
USERCTL=no
```


- Mẫu cloud-init. đối với ubuntu user mặc định sẽ là ubuntu, đối với CentosOS user mặc định sẽ là root
```
#cloud-config
password: nautilus2020
chpasswd: { expire: False }
ssh_pwauth: True
```


```
## https://docs.openstack.org/image-guide/create-images-manually.html

```