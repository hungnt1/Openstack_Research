
# OpenStack Dashboard - Horizon

# 1. Tổng quan về Horizon

## 1.1. Khái niệm Horizon

- Horizon là code-name của Openstack Dashboard , cung cấp một Web-based interface cho các Openstack Service khác nhau gồm : Nova, Swift, Keystone, etc... 
- Horizon sử dụng Django Python làm việc với các API Service, sử dụng openstack indentify để authen , không sử dụng database riêng 

## 1.2 . Chức năng chính của Horzion
- Cung cấp giao diện quản lý dễ dàng
- Có thể sử dụng cho môi trường production
- Tùy chỉnh, thêm các compoment vào panel theo từng dịch vụ
- Quy trình làm việc trong suốt với người dùng
- Code-base theo hướng đối tượng, dễ phát triển

## 1.3 . Kiếm trúc làm việc với các Service khác

![](https://access.redhat.com/webassets/avalon/d/Red_Hat_Enterprise_Linux_OpenStack_Platform-7-Architecture_Guide-en-US/images/05df8dacdfb319319665befc022e4159/RHEL_OSP_arch_347192_1015_JCS_02_Interface-Dashboard.png)


## 2. Các thành phần trên Dashboard Tab

# 2.1 . Compute Tab

- Overview : xong báo cáo tổng quan về project
- Instance : quản lý vòng đời của các mảy ảo, kết nối máy ảo qua console
- Volume : quản lý vòng đời các volume và snapshot volume
- Image : liệt kê các image, instance snapshot, volume snapshot và quản lý vòng đời của chúng
- Access & Security : quản lý vòng đời security group, key pair, floating IP, API access request

# 2.2. Network Tab

- Network topology : tổng quan về mô hình mạng đang có sẵn
- networs : quản lý vòng đời các mạng ảo
- route : khởi tạo các điểm routing

# 2.3. Identity Tab

-   **Projects**  : quản lý vòng đời các project, xem thống kê của project, quản lý các user
-   **Users**  : quản lý user,  hiển thị thông báo nếu không có đặc quyền

# 3. Tham khảo thêm

[1] : https://access.redhat.com/documentation/en-us/red_hat_openstack_platform/8/html-single/introduction_to_the_openstack_dashboard/index
[2] : https://docs.openstack.org/horizon/latest/
