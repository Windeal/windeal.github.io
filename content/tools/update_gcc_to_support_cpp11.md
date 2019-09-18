Title: gcc升级的简单方法
Date: 2017-06-16
Category: tools
Tags: gcc, C++11
Slug: update_gcc_to_support_cpp11
Authors: windealli
Summary: gcc 升级到4.9的简单方法。支持C++11

## gcc 升级

升级gcc目前知道两种方法

+ 直接编译安装新版本的gcc （目测前方坑很多）
+ 安装devtoolset来升级gcc， （网上说这种方式很简单）

下面通过devtoolset来升级下gcc devtoolset目前有4个版本:devtoolset-1.1 devtoolset-2 devtoolset-3 devtoolset-4， 以上版本分别对应gcc的版本为4.7、4.8、4.9、5.2。

gcc 4.8好像就完全支持C++11了， 安全起见，我打算安装gcc 4.9 下面是升级步骤
```
yum install centos-release-scl-rh centos-release-scl
yum check-update
yum install devtoolset-3-gcc  devtoolset-3-gcc-c++
```

升级之后需要启动devtoolset：

`source /opt/rh/devtoolset-3/enable `测试发现当前命令似乎只对本次shell有效，所以可能需要把这条命令加入到~/.bashrc中。

接下来可以通过`gcc -v `查看是否更新完毕。