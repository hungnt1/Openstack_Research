
# OpenStack Block Storage - Cinder

# 1. Tổng quan về Cinder

## 1.1. Khái niệm Cinder

- Cinder là code-name cho Openstack Block Storage. Nó được thiết kế với khả năng lưu trữ dữ liệu mà người dùng cuối có thể sử dụng bỏi Project Compute (NOVA). Nó có thể được sử dụng thông qua các reference implementation (LVM) hoặc các plugin driver dành cho lưu trữ.
- Có thể hiểu ngắn gọn về Cinder như sau : Cinder là ảo hóa việc quản lý các thiết bị Block Storage và cung cấp cho người dùng một API đáp ứng được như cầu tự phục vụ cũng như yêu cầu tiêu thụ các tài nguyên đó mà không cần có quá nhiều kiến thức về lưu trữ.

## 1.2. Các chức năng chính
-   Cung cấp và quản lý các tài nguyên lưu trữ dạng persistent block storage (volume) cho các máy ảo
-   Các volume này có thể được tách từ máy ảo này và gán lại vào một máy ảo khác, mà dữ liệu được giữ nguyên không bị thay đổi.
-   Hiện tại, một volume chỉ có thể được gán (attached) và một máy ảo tại một thời điểm
-   Các volume tồn tại độc lập với các máy ảo (tức là khi máy ảo bị xóa thì volume không bị xóa).
-   Phân chia tài nguyên lưu trữ thành các khối gọi là Cinder volume.
-   Cung cấp các API như là tạo, xóa, backup, restore, tạo snapshot, clone volume và nhiều hơn nữa. Những API này thực hiện bởi các backend lưu trữ mà được cinder hỗ trợ.
-   Các kiến trúc plugin drive cho phép nhiều lựa chọn làm backend storage.

## 1.3. Lợi ích chính
- Cinder cung cấp block storage dưới dạng `block as a service`
	-  **Component based architecture**: thực hiện một hành động mới dễ dàng
	-   **Highly available**: tỉ lệ % công việc được chia nhỏ 
	-   **Fault-Tolerant**: các tiến trình được tách riêng biệt
	-   **Recoverable**: dễ dàng phán đoán, sửa lỗi 
	-   **Open Standards**: cộng đồng API mở 


# 2. Kiến trúc trong Cinder

![](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux_OpenStack_Platform/6/html/Component_Overview/images/interfaces_blockStorage.png)

- openstack-cinder-volume : quản lý vòng đời volume cho các máy ảo theo yêu cầu . Khi có một request từ sheduler , volume service sẽ tạo, chỉnh sửa, xóa các volume theo yêu cầu. Một số các driver sẽ được sử dụng để làm việc với storage provider
- openstack-cinder-api : trả lời và xử lý theo yêu cầu, gửi các tin nhắn vào hàng chờ . Khi có một request gửi đến, các API nhờ indentify service để xác thực , sau đó gửi thông điệp để làm việc với các block storage. 
- openstack-cinder-backup : cung cấp khả năng backup các Storage Voluem sang một repo khác 
- openstack-cinder-sheduler : gửi các task vào hàng chờ , và xác định volume server. Sheduler sẽ nhận các bản tin từ hàng chờ sau đó xác định block storage host sẽ làm việc . 
- Database : lưu thạng trái các volume 
- RabbitMQ server : cung cấp hàng chờ tin nhắn AMQP, RabbitMQ làm việc với các các Openstack Copoment khác : hàng chờ, phân phối,, quản lý, bảo mật liên kết2x


# 3. Các thành phần trong Cinder
-  Back-end storage device : yêu cầu một số back-end storage service.  Mặc định Cinder tích hợp và sử dụng với LVM, trên một logical volume group có tên `cinder volume`. Ngoài việc sử dụng LVM, tra có thể sử dụng nhiều drvier khác để làm việc với Cinder như Raid hoặc các driver lưu trữ khác. Những back-end driver này có thể tùy chỉnh block size khi  sử dụng KVM-QEMU làm hypersvisor

- Users and Tenants (Projects) : dịch vụ Block Storage có thể được sử dụng bởi nhiều khách hàng hoặc khách hàng điện toán đám mây khác nhau (những tenant trên một hệ thống shared system), sử dụng gán quyền truy cập theo role. Các role điểu khiển các hành động mà người dùng được phép thực hiện. Trong cấu hình mặc định, hầu hết các hành động không yêu cầu role cụ thể, nhưng điều này có thể được cấu hình bởi quản trị viên hệ thống trong tệp `policy.json`thích hợp để duy trì các quy tắc. Quyền truy cập vào một volume cụ thể của người dùng bị giới hạn bởi tenant (project), nhưng tên người dùng và mật khẩu được chỉ định cho mỗi người dùng. Các cặp khóa key-pairs cho phép truy cập vào một volume được kích hoạt cho mỗi người dùng, nhưng hạn ngạch quotas để kiểm soát tài nguyên sử dụng trên các thiết bị phần cứng có sẵn là cho mỗi tenant. 

- Volume, Snapshots và Backups : 
	- Volume : gắn các blcok storage đã được phân bổ vào các instance, hoạt động như một storage thứ 2 cho các instance hoặc như root filesystem storage để làm boot disk cho instance.  Các volume là các thiết bị lưu trữ  dưới dạng Read/Write   được gắn vào các compute node sử dụng iSCSI. 
	- Snapshot : một bản read-only dữ trữ dữ liệu của volume tạo một thời điểm nào đó . Snapshot có thể khởi tạo cho một volume đang ở trạng thái active nếu sử dụng `--force True`
	- Backup : bản copy của một volume lưu trữ trên Object Storage ( Swift ) 

# 4. Tham khảo thêm
[1] : https://github.com/hocchudong/thuctap012017/blob/master/TamNT/Openstack/Cinder/docs/Tong_quan_Cinder.md

[2] : https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux_OpenStack_Platform/6/html/Component_Overview/section-blockStorage.html

[3] : https://docs.openstack.org/cinder/latest/configuration/block-storage/block-storage-overview.html
