

- Tập tin cấu hình Corosync
```
totem {
    version: 2
    cluster_name: hacluster
    secauth: off
    transport: udpu
}

nodelist {
    node {
        ring0_addr: 192.168.69.130
        nodeid: 1
    }

    node {
        ring0_addr: 192.168.69.131
        nodeid: 2
    }

    node {
        ring0_addr: 192.168.69.132
        nodeid: 3
    }
}

quorum {
    provider: corosync_votequorum
}

logging {
    to_logfile: yes
    logfile: /var/log/cluster/corosync.log
    to_syslog: yes

```
