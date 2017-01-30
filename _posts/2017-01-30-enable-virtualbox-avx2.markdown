---
layout: post
title: Enable VirtualBox AVX2
date: 2017-01-30 17:06:33 +0800
categories: 
---

1. Check cpuflags: use `cat /proc/cpuinfo` on GNU/Linux, 
  or check `Structured Extended Feature Flags Enumeration` section 
  in VirtualBox log(VBox.log); AVX2 could be enabled only if cpu has AVX2 flag.
2. Execute  `vboxmanage setextradata "VM_NAME" VBoxInternal/CPUM/IsaExts/AVX2 1`,
   replace "VM_NAME" with your name of VM to enable AVX2. If you're running VM on 
   Windows host, `vmboxmanage` is in the installation directory of VirtualBox,
   the same folder of `VirtualBox.exe`.
3. Just boot your VM to check if AVX2 is enabled.

Reference: [AskUbuntu](http://askubuntu.com/questions/699077/how-to-enable-avx2-extensions-on-a-ubuntu-guest-in-virtualbox-5)