
## Packstack - Openstack

# 1. Giới thiệu Packstack
Packstack là một bộ command-line sử dụng Puppet ([http://www.puppetlabs.com/](http://www.puppetlabs.com/)) module để triển khai nhanh Openstack thông qua kết nối SSH.  Packstack rất thích hợp triển khai cho cả single node và multi node. 
Hiện tại Packstack chỉ hỗ trợ `Centos` và `Redhat Enterprise Linux [RHEL]`	. Ưu điểm lớn nhất của Packstack là triển khai hạ tầng nhanh chóng , sử dụng để demo , phát triển chức năng, nhưng ưu điểm của packstack là trong suốt với người dùng, việc triển khai hoàn toàn tự động.


# 2. Triển khai Packstack

## 2.1 . Mô hình, phân bổ IP, môi trường triển khai
![](https://i.imgur.com/ogdwTbG.png)

Môi trường
- OS : Centos 7.5
- Version : Openstack Queens 

## 2.2 . Yêu cầu phần cứng tối thiểu

- Controller Node 
	-  2GB RAM 
	- 50GB disk avaliable
	- 2 NIC

- Compute Node
	- Kiểm tra extension ảo hóa
	`grep -E 'svm|vmx' /proc/cpuinfo | grep nx`
	Nếu có ouput thì server đã hỗ trợ ảo hóa
	- 2GB RAM
	- 50GB Disk avaliable
	- 2 NIC


## 2.3 . Cấu hình IP  cho các Compute node

- Login vào Controller Node , thực hiện lệnh sau dưới root account
- Thiết lập hostname , IP trên tất cả Node
```bash
#!/bin/bash -ex
controller_name="controller"
host1_name="host1"
host2_name="hosts2"
controller=("ens192"  "ens224"  "192.168.30.130"  "192.168.30.1"  "192.168.69.130")
host1=("ens192"  "ens224"  "192.168.30.131"  "192.168.30.1"  "192.168.69.131")
host2=("ens192"  "ens224"  "192.168.30.132"  "192.168.30.1"  "192.168.69.132")
echo  "${controller[0]}"
function  set_controller(){
# nmcli d modify ${controller[0]} ipv4.address ${controller[2]}
# nmcli d modify ${controller[0]} ipv4.gateway ${controller[3]}
# nmcli d modify ${controller[0]} ipv4.dns 1.1.1.1
# nmcli d modify ${controller[0]} ipv4.method manual
# nmcli d modify ${controller[0]} down
# nmcli d modify ${controller[0]} up
# nmcli d modify ${controller[0]} connection.autoconnect yes
echo  "Setup IP Management Card"
systemctl start NetworkManager
ip link set  ${host1[1]} up
nmcli d modify ${controller[1]} ipv4.address ${controller[4]}
nmcli d modify ${controller[1]} ipv4.method manual
nmcli d modify ${controller[1]} connection.autoconnect yes
systemctl stop NetworkManager
service network restart
echo  "Done Set IP controller"
}
function  set_host1 {
# echo  "Setup IP External Card ${host1_name}"
# ip link set  ${host1[1]} up
# nmcli d modify ${host1[0]} ipv4.address ${host1[2]}/24
# nmcli d modify ${host1[0]} ipv4.gateway ${host1[3]}
# nmcli d modify ${host1[0]} ipv4.dns 1.1.1.1
# nmcli d modify ${host1[0]} ipv4.method manual
# nmcli d modify ${host1[0]} connection.autoconnect yes
echo  "Setup IP Management Card ${host1_name} "
systemctl start NetworkManager
ip addr flush ${host1[1]}
ip link set ${host1[1]} up
nmcli d modify ${host1[1]} ipv4.address ${host1[4]}/24
nmcli d modify ${host1[1]} ipv4.method manual
nmcli d modify ${host1[1]} connection.autoconnect yes
systemctl disable firewalld
systemctl stop firewalld
systemctl stop NetworkManager
service network restart
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux
}
function  set_host2 {
# echo  "Setup IP External Card ${host2_name}"
# ip link set  ${host2[0]} up
# nmcli d modify ${host2[0]} ipv4.address ${host2[2]}/24
# nmcli d modify ${host2[0]} ipv4.gateway ${host2[3]}
# nmcli d modify ${host2[0]} ipv4.dns 1.1.1.1
# nmcli d modify ${host2[0]} ipv4.method manual
# nmcli d modify ${host2[0]} connection.autoconnect yes
echo  "Setup IP Management Card ${host2_name}"
ip addr flush ${host2[1]}
ip link set  ${host2[1]} up
nmcli d modify ${host2[1]} ipv4.address ${host2[4]}/24
nmcli d modify ${host2[1]} ipv4.method manual
nmcli d modify ${host2[1]} connection.autoconnect yes
sudo systemctl disable firewalld
sudo systemctl stop firewalld
systemctl stop NetworkManager
service network restart
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/selinux/config
sed -i 's/SELINUX=enforcing/SELINUX=disabled/g' /etc/sysconfig/selinux
reboot
}
echo  "------------- Setting Controller ------------- "
set_controller
echo  "------------- Connect To Host 1 ------------- "
echo  "------------- Done ---------------------------"
ssh root@192.168.30.131 -t "$(typeset -f);\
host1_name="host1" ; host1=("ens192" "ens224" "192.168.30.131" "192.168.30.1" "192.168.69.131"); set_host1"
echo  "------------- Done ---------------------------"
echo  "------------- Connect To Host 2 ------------- "
ssh root@192.168.30.132 -t "$(typeset -f);\
host1_name="host1" ; host2=("ens192" "ens224" "192.168.30.132" "192.168.30.1" "192.168.69.132"); set_host2"
echo  "------------- Done ---------------------------"
```


### 2.4.  Cài đặt Packstack 

Một số lưu ý khi cài đặt
- Sử dụng tài khoản, tài khoản root để thực hiện
- Thực hiện trên Controller Node
- Trong lúc thực hiện, sẽ yêu cầu password của các  Compute Node tham giaf
- Quá trình cài đặt sẽ tự động hoàn toàn
- Cài đặt packstack Queens
```bash
yum install -y centos-release-openstack-queens epel-release
yum install -y openstack-packstack python-pip

echo "------------------Cau hinh tong quan------------------"
packstack --gen-answer-file=/root/queens-answer.txt
sed -i "s/CONFIG_COMPUTE_HOSTS=.*/CONFIG_COMPUTE_HOSTS=192.168.69.131,192.168.69.132/g" /root/queens-answer.txt
sed -i "s/CONFIG_PROVISION_DEMO=.*/CONFIG_PROVISION_DEMO=n/g" /root/queens-answer.txt
sed -i "s/CONFIG_KEYSTONE_ADMIN_PW=.*/CONFIG_KEYSTONE_ADMIN_PW=123@123Aa/g" /root/queens-answer.txt
sed -i "s/CONFIG_DEFAULT_PASSWORD=.*/CONFIG_DEFAULT_PASSWORD=123@123/g" /root/queens-answer.txt
echo "------------------Cau hinh external network-----------"
sed -i "s/CONFIG_NEUTRON_OVS_BRIDGE_IFACES=.*/CONFIG_NEUTRON_OVS_BRIDGE_IFACES=br-ex:ens192/g" /root/queens-answer.txt
sed -i "s/CONFIG_HORIZON_SSL=.*/CONFIG_HORIZON_SSL=y/g" /root/queens-answer.txt
sed -i "s/192.168.30.130/192.168.69.130/g" /root/queens-answer.txt
echo "-----------------------DONE---------------------------"
echo "-----------------------Cai dat------------------------"
packstack --answer-file=/root/queens-answer.txt

```

- Sau khi chạy script, quá trình cài đặt tự động 	bắt đầu
![](https://i.imgur.com/PQV5gyf.png)
![](https://i.imgur.com/vPwO8NV.png)


- Sau khi cài đặt xong, truy cập vào IP MGT của Controller để sử dụng Horizon
![](https://i.imgur.com/q7sj1QW.png)






## 2.5. Làm việc với command-line

- Sau khi cài đặt thành công packstack, tại thư mục root sẽ có 2 file openrc, cung cấp 2 tài khoản `admin` và `demo`. Để có thể sử dụng tài khoản `admin` để xác thực ta cần thực thi các biến môi trường
```
[root@controller ~] source ~/keystonerc_admin
[root@controller ~(keystone_admin)]# openstack token issue
+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Field      | Value                                                                                                                                                                                   |
+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| expires    | 2018-10-31T05:35:02+0000                                                                                                                                                                |
| id         | gAAAAABb2TD2l-Uwo_lwKNce9tny9FkhVUi--Toar88dWJ8LgmjYNF20EbnmQgF9yImqfQt0B6cvfgzw9EapVRkzVbx7DW0LK57jtiFtnT9_G34Lx5Y9oNGE0EcaEdIepBH_j5FQ2xXSnzApCrR1sa0KqR8ikRxpZWaWJnVAsq9Kq9bEns2qb3A |
| project_id | fc2293ba8d44415b8cdbf86d0e70216a                                                                                                                                                        |
| user_id    | 0dc173d110e4435ab74440adcfdd505f                                                                                                                                                        |
+------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
[root@controller ~(keystone_admin)]# 

```

- Upload image lên glance
```
wget http://download.cirros-cloud.net/0.3.4/cirros-0.3.4-x86_64-disk.img
openstack image create "cirros" \
	  --file cirros-0.3.4-x86_64-disk.img \
	  --disk-format qcow2 --container-format bare \
	  --public
```

- Khởi tạo network external
```
neutron net-create external_network --provider:network_type flat \
--provider:physical_network extnet  \
--router:external \
--shared
```

- Khởi tạo subnet cho network external
```
neutron subnet-create --name ex_subnet --gateway 192.168.30.1 \
--allocation-pool start=192.168.30.140,end=192.168.30.150 \
--enable-dhcp=True external_network 192.168.30.0/24
```

- Khởi tại self-servivce nework và subnet
```
neutron net-create self-net
neutron subnet-create --name self-subnet self-net 10.20.20.0/24
```

- Khởi tạo router
```
neutron router-create ex_router 
neutron router-gateway-set ex_router  external_network
neutron router-interface-add ex_router self_subnet

```

- Kiểm tra Port List trên các network vừa tạo
```
[root@controller ~(keystone_admin)]# neutron port-list
neutron CLI is deprecated and will be removed in the future. Use openstack CLI instead.
+--------------------------------------+------+----------------------------------+-------------------+---------------------------------------------------------------------------------------+
| id                                   | name | tenant_id                        | mac_address       | fixed_ips                                                                             |
+--------------------------------------+------+----------------------------------+-------------------+---------------------------------------------------------------------------------------+
| 03a5b603-ead6-4ace-826e-ff4fa5ee1412 |      | fc2293ba8d44415b8cdbf86d0e70216a | fa:16:3e:61:ec:72 | {"subnet_id": "34dc94de-4884-45fb-9732-2705a79fb798", "ip_address": "10.20.20.1"}     |
| 9075b501-104d-4215-845c-ba5ce8f2a060 |      |                                  | fa:16:3e:bf:4f:dc | {"subnet_id": "449db0ad-6e9f-4b96-9927-09b4006e98d8", "ip_address": "192.168.30.148"} |
| aef9a689-f270-4a0c-9f3c-5e4b9028269b |      | fc2293ba8d44415b8cdbf86d0e70216a | fa:16:3e:bd:8d:18 | {"subnet_id": "34dc94de-4884-45fb-9732-2705a79fb798", "ip_address": "10.20.20.2"}     |
| d9f6cbee-2307-4b4d-bdcc-a3b440290edb |      | fc2293ba8d44415b8cdbf86d0e70216a | fa:16:3e:f0:ed:31 | {"subnet_id": "449db0ad-6e9f-4b96-9927-09b4006e98d8", "ip_address": "192.168.30.140"} |
+--------------------------------------+------+----------------------------------+-------------------+------------------------------------------

```
- Ping đến IP trong port list provider
```
[root@controller ~(keystone_admin)]# ping 192.168.30.140
PING 192.168.30.140 (192.168.30.140) 56(84) bytes of data.
64 bytes from 192.168.30.140: icmp_seq=1 ttl=64 time=0.673 ms
64 bytes from 192.168.30.140: icmp_seq=2 ttl=64 time=0.111 ms
64 bytes from 192.168.30.140: icmp_seq=3 ttl=64 time=0.085 ms
64 bytes from 192.168.30.140: icmp_seq=4 ttl=64 time=0.079 ms
64 bytes from 192.168.30.140: icmp_seq=5 ttl=64 time=0.082 ms
64 bytes from 192.168.30.140: icmp_seq=6 ttl=64 time=0.101 ms
64 bytes from 192.168.30.140: icmp_seq=7 ttl=64 time=0.058 ms
64 bytes from 192.168.30.140: icmp_seq=8 ttl=64 time=0.043 ms

```
## 2.56. Thao tác với Dashboard

- Dashboard của Packstack có thể truy cập tại `192.168.30.130/dashboard`
![](https://i.imgur.com/JqqKdBi.png)

- Tạo máy ảo 
![](https://i.imgur.com/VNV0yAX.png)

![](https://i.imgur.com/2uWbERs.png)
![](https://i.imgur.com/1MZHqqU.png)
