---
layout: post
title: 华为AR-160部署L2TP/IPSec
date: 2021-11-11 16:30:00 +0800
categories: 
---

## 免责声明
本人对计算机网络、华为路由器都不熟悉，本文中的操作以及观点仅供参考。如有事实错误，欢迎通过Github 
issues指正。

## 概述
AR路由器有两种配置方式：Web和命令行。Web现在还不能直接配置L2TP/IPSec，只能简单配置（朴素）L2TP。然而朴素的L2TP安全性是不足的[^1]，现代的操作系统（Windows/macOS/Android/iOS）都不支持朴素L2TP，而是支持L2TP/IPSec（L2TP over IPSec），即先利用IPSec建立安全通信后，再加密地建立L2TP连接。

也就是说，配置L2TP/IPSec必须要使用命令行的方式。你至少需要一个有超级管理员权限的路由器账号，并且确保路由器能够远程登录管理（比如使用SSH）。

我的场景是，组织内的以太网设备都接入AR路由器LAN接口，AR路由器通过WAN接口拨号接入广域网，并且具有公网IP。组织的成员会在广域网上通过L2TP/IPSec接入公司局域网。这样的需求和这份[华为配置案例]中的描述基本一致，在此不再赘述。

## 细节（坑）
问题大多出现在建立IPSec连接中。但是网络上能参考的文档极少，华为官方文档[^2]中给出解决方法大多没有用。实际部署过程中，遇到的坑有三个：

### 接口问题
IPSec policy是需要附加在接口上的，如果通过拨号上网方式接入广域网，是需要挂在拨号用的虚拟接口上的（比如`Dialer1`）。

### macOS/iOS无法连接
花费了大量时间排查。已经不记得最一开始是从哪里看到的了，但是在这份[路由器文档]里也有描述。华为路由器使用的SHA2算法似乎默认并不符合RFC。要使用文档中`ipsec authentication sha2 compatible enable`命令，强制使用兼容RFC的SHA2算法，苹果系操作系统才能连接上。

### Windows 10无法连接
我在Windows上只有Windows 10这一版本的需求。自从Windows 8.1以来，Windows在“设置”里就开始自带VPN客户端。但是这一客户端并不能直接进行高级配置，然而这一点很重要。所谓的高级配置就是指定IPSec建立连接时使用的密码学算法（SHA、AES等）以及密钥长度。如果客户端与服务端在这些参数上不统一，就无法建立安全连接。Windows 10上配置这些参数，需要通过PowerShell命令行的方式。

首先，还是通过Windows设置，先创建好一个L2TP/IPSec连接（网络适配器）。建立好连接后，执行如下命令：
```powershell
Set-VpnConnectionIPsecConfiguration -ConnectionName "你的连接名称" `
    -AuthenticationTransformConstants SHA256128 `
    -CipherTransformConstants AES256 -EncryptionMethod AES256 `
    -IntegrityCheckMethod SHA256 -PfsGroup None -DHGroup Group14 `
    -PassThru -Force
```
需要指出的是，`AuthenticationTransformConstants`*应该（我不确定）*与IPSec policy中的“ESP认证算法”对应，我选用的是`SHA2-256`，命令行中就选用了`SHA256128`。其他命令行参数参考这份[微软文档]即可。


[^1]: See this [L2TP Wiki](https://en.wikipedia.org/wiki/Layer_2_Tunneling_Protocol#Description)

[^2]: 华为给出的[IPSec troubleshooting]和[L2TP troubleshooting]。

[华为配置案例]: https://support.huawei.com/hedex/pages/EDOC1100021771AZH05262/13/EDOC1100021771AZH05262/13/resources/dc/dc_ar_cc_l2tp_0003.html?ft=0&fe=10&hib=7.3.6.1.8&id=ZH-CN_TASK_0177893105&text=%25E9%2585%258D%25E7%25BD%25AE%25E8%25BF%259C%25E7%25A8%258B%25E6%258B%25A8%25E5%258F%25B7%25E7%2594%25A8%25E6%2588%25B7%25E9%2580%259A%25E8%25BF%2587L2TP%2520over%2520IPSec%25E6%2596%25B9%25E5%25BC%258F%25E6%258E%25A5%25E5%2585%25A5%25E6%2580%25BB%25E9%2583%25A8%25E7%259A%2584%25E7%25A4%25BA%25E4%25BE%258B&docid=EDOC1100021771

[路由器文档]: https://support.huawei.com/hedex/pages/EDOC1100021771AZH05262/13/EDOC1100021771AZH05262/13/resources/dc/ipsec_authentication_sha2_compatible_enable.html?ft=0&fe=10&hib=9.12.6.94&id=ipsec_authentication_sha2_compatible_enable&text=ipsec%2520authentication%2520sha2%2520compatible%2520enable&docid=EDOC1100021771

[微软文档]: https://docs.microsoft.com/en-us/powershell/module/vpnclient/set-vpnconnectionipsecconfiguration?view=windowsserver2019-ps

[IPSec troubleshooting]: https://support.huawei.com/enterprise/en/doc/EDOC1100086053

[L2TP troubleshooting]: https://support.huawei.com/enterprise/en/doc/EDOC1100176155