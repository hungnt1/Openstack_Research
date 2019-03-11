

Ghi chép quá trình tìm hiểu OpenStack
- Creator : Nguyen Trong Hung
- Môi trường : Centos 7.5
- Phiên bản : Openstack Queens
- Hypervisor : KVM/QEMU
- Có sử dụng FirewallD, không sử dụng SeLinux (   permissive mode ) 

## Mục Lục

## 1. Giới thiệu

- [Giới thiệu về Cloud Computing và Openstack](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/1.%20Intro%20Cloud%20Computing.md)

- [Cài thử nghiệm Openstack sử dụng Packstack](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/2.install-pack-stack.md)
### 2. Keystone

- [Giới thiệu về  Openstack  Identity](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Keystone/1.%20Introduction-Keystone.md)
- [Cài đặt Keystone ](https://github.com/nguyenhungsync/Openstack_Research/blob/master/Keystone/2.Install-Keystone.md)
- [Các tùy chọn trong Keystone](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Keystone/4.%20Config-Keystone.md)
- [Làm việc với Keystone](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Keystone/5.%20Keystone-Openstack-CLI.md)
- [Làm việc với Keystone (2) ]( https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Keystone/6.%20Keystone-CURL.md)
- [Token trong Keystone](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Keystone/7.%20Token-Keystone.md)

### 3. Glance

- [Giới thiệu về Openstack Image Service](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Glance/1.%20Introduction-Glance.md)
- [Cài đặt Glance](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Glance/2.%20Install%20Glance.md)
- [Làm việc với Glance](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Glance/3.%20Openstack-Glance-%26-CURL.md)
- [Các tùy chọn trong Glance](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Glance/4.%20Config.md)
- [Các quá trình trong Glance](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Glance/5.%20Glance-Advanced.md)

### 4. Nova

- [Giới thiệu về Openstack Compute Service](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Nova/1.Introduction-nova.md)
- [Cài đặt Nova](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Nova/2.%20Install-nova.md)
- [Làm việc với Nova](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Nova/3.Nova-Client%26Curl.md)
- [Các quá trình trong Nova](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Nova/4.%20Nova-Instance-Work-flow.md)
- [Debug](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Nova/5.%20Debug.md)
- [Các cấu hình trong Nova](https://github.com/nguyenhungsync/Openstack_Research/blob/master/Nova/6.%20Config-section.md)
### 5. Neutron

- [Giới thiệu về Neutron](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Neutron/1.%20Introduction-neutron.md)
- [Cài đặt Neutron Linux Bridge - Self-Service](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Neutron/2.%20Install%20Neutron%20Linux%20Bridge.md)
- [Cài đặt Neutro OVS - Self-Service](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Neutron/2.1%20.%20OVS-Self-Services.md)
- [Cài đặt Neutron OVS - Provider](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Neutron/2.2.%20OVS%20Self-Service-%26-Provider.md)
- [Làm việc với Neutron ](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Neutron/3.%20Neutron-CLI.md)
- [Tìm hiểu các Namespace, Agent trong Neutron](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Neutron/4.%20Neutron-Namespace-Agent.md)
- [Packet Flow sử dụng Linux Bridge](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Neutron/5.%20%20Packet-Walkthrough-Linux-Bridge.md)
- [Cấu hình Bonding](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Neutron/6.%20Bonding.md)
- [Tìm hiểu VXLAN](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Neutron/7.%20VXLAN.md)
- [Tìm hiểu OpenvSwitch trong OPS](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Neutron/8.%20OVS.md)
- [Packet Flow sử dụng OpenvSwitch - Self Service ](https://github.com/nguyenhungsync/Openstack_Research/blob/master/Neutron/9.%20OPS-Packet-Self-Service.md)
- [Packet Flow sử dung OpenvSwitch - Provider ](https://github.com/nguyenhungsync/Openstack_Research/blob/master/Neutron/10.%20OPS-Packet-Provider.md)

## 6. Cinder

- [Giới thiệu về Cinder](https://github.com/nguyenhungsync/Openstack_Research/blob/master/Cinder/1.%20Introduction-cinder.md)
- [Mối quan hệ giữa instance và disk ](https://github.com/nguyenhungsync/Openstack_Research/blob/master/Cinder/2.%20Cinder-Disk-Work-Flow.md)
- [Cài đặt Cinder sử dụng LVM backend](https://github.com/nguyenhungsync/Openstack_Research/blob/master/Cinder/3.%20Install-Cinder-LVM.md)
- [Cài đặt Cinder sử dụng LVM và NFS](https://github.com/nguyenhungsync/Openstack_Research/blob/master/Cinder/5.%20Install-Multi-Backend.md)
- [Sử dụng Cinder cơ bản](https://github.com/nguyenhungsync/Openstack_Research/blob/master/Cinder/4.%20Basic-Command.md)
- [Filter trong Multi Backend Cinder](https://github.com/nguyenhungsync/Openstack_Research/blob/master/Cinder/6.%20Filtering-Multi-Backend.md)

## 7. HA Proxy và KeepAlived

- [Giới thiệu về HA, HA Proxy và Keep Alived](https://github.com/nguyenhungsync/Openstack_Research/blob/master/High-availability/1.HA-Proxy---KeepAlive/1.Intro.md)
- [Cài đặt HA Proxy và Keep Alived](https://github.com/nguyenhungsync/Openstack_Research/blob/master/High-availability/1.HA-Proxy---KeepAlive/2.%20Setup-HA-Proxy-%26%26-KeepAlive.md)
- [Cài đặt HA Proxy và Keep Alived trên Openstack VM](https://github.com/nguyenhungsync/Openstack_Research/blob/master/High-availability/1.HA-Proxy---KeepAlive/3.HA-Proxy-OPS.md)

## 8. Barbican

- [Giới thiệu và cài đặt Barbican ](https://github.com/nguyenhungsync/Openstack_Research/blob/master/Barbican/1.%20Intro-Setup.md)
- [Thao tác cơ bản với Barbican](https://github.com/nguyenhungsync/Openstack_Research/blob/master/Barbican/1.%20Intro-Setup.md)

## 9. Octavia

- [Giới thiệu và cài đặt Octavia Single](https://github.com/nguyenhungsync/Openstack_Research/blob/master/High-availability/2.%20Octavia/1.Intro%2BSetup.md)
- [Sử dụng Octavia Self-Service](https://github.com/nguyenhungsync/Openstack_Research/blob/master/High-availability/2.%20Octavia/2.Use-Octavia.md)
- [Cài đặt , sử dụng Octavia Provider && Deep Dive Amphora VM](https://github.com/nguyenhungsync/Openstack_Research/blob/master/High-availability/2.%20Octavia/3.%20Octavia-Keep-Alived.md)
- [Sử dụng Octaiva VIP QOS](https://github.com/nguyenhungsync/Openstack_Research/blob/master/High-availability/2.%20Octavia/4%20.VIP-QOS.md)
- [Lý thuyết Octavia L7 Policy](https://github.com/nguyenhungsync/Openstack_Research/blob/master/High-availability/2.%20Octavia/5.Theory-Octavia-L7-Policy.md)
- [Sử dụng Octavia L7 Policy](https://github.com/nguyenhungsync/Openstack_Research/blob/master/High-availability/2.%20Octavia/6.%20LAB-Octavia-L7-Policy.md)
### 10. Mở rộng

- [Key Rorate và Decrypt trong Keystone](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Advance/1.%20Key-Rotate-%26-Decrypt.md)
- [Sử dụng RabbitMQ và Endpoint trong Openstack](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Advance/2.RabbitMQ-%26-API-Endpoint.md)
- [Log trong Openstack](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Advance/3.%20Log.md)
- [Cấu hình noVNC Node](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Advance/4.%20Setup-noVNC.md)
- [Liên hệ giữa Nova-Compute và RabbitMQ](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Advance/5.%20Nova-Compute-Serice-%26-RabbitMQ.md)
- [Placment API và Nova Conductor trong Openstack](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Advance/6.%20Placement-API-%26-Nova-Conductor.md)
- [Quản lý tài nguyên trong Nova](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Advance/7.1.%20%20Resource-Management-OPS.md)
- [Nova-Scheduler và Filter trong Nova](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Advance/7.2%20.%20Nova-Scheduler-%26-Host-Aggreaggregate.md)
- [Host Aggregate trong Nova-Scheduler](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Advance/7.3.%20Lab-Filter-Scheduler.md)
- [Resize instance](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Advance/8.%20Resize-instance.md)
- [Recuse instnace](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Advance/9.%20Rescue-instance.md)
- [Giới hạn CPU Resource trong Nova](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Advance/10.%20Limit-CPU-Resource.md)
- [Metadata](https://github.com/nguyenhungsync/Report-Intern-Meditech/blob/master/Openstack/Advance/11.%20Metadata.md)

- [Cấu hình VXLAN OVS Tunnel](https://github.com/nguyenhungsync/Openstack_Research/blob/master/Neutron/11.%20VXLAN-Tunnel.md)
- [Cấu hình join VXLAN Tunnel Openstack](https://github.com/nguyenhungsync/Openstack_Research/blob/master/Neutron/11.%20VXLAN-Tunnel.md)
- [Tìm hiểu Cloud Init](https://github.com/nguyenhungsync/Openstack_Research/blob/master/Advance/12.%20Cloud-init.md)
- [Tìm hiểu Cloud INIT -2 ](https://github.com/nguyenhungsync/Openstack_Research/blob/master/Advance/13.%20Cloud-init-Script.md)
- [Tìm hiểu QOS trong Neutron](https://github.com/nguyenhungsync/Openstack_Research/blob/master/Advance/14.%20QOS%20-%20Neutron.md)
- [Tìm hiểu QOS trong Cinder](https://github.com/nguyenhungsync/Openstack_Research/blob/master/Advance/15.%20QOS%20-%20Cinder.md)
- [Tìm hiểu Cinder Backup sử dụng NFS](https://github.com/nguyenhungsync/Openstack_Research/blob/master/Advance/16.%20Cinder-Backup-NFS.md)
- [Tìm hiểu Transfer và Extend Volume](https://github.com/nguyenhungsync/Openstack_Research/blob/master/Advance/17.%20Transfer-%26-Extend-Root-Volume.md)
- [Tìm hiểu cấu hình HA L3 Agent trên các Compute Node](https://github.com/nguyenhungsync/Openstack_Research/blob/master/Advance/18.%20L3-Agent-HA-Compute.md)
- [Tìm hiểu VM Password](https://github.com/nguyenhungsync/Openstack_Research/blob/master/Advance/20.%20Nova-password.md)


