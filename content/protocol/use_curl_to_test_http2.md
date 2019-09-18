Title: 使用curl进行http2测试
Date: 2017-06-9
Category: protocol
Tags: Http2, curl
Slug: use_curl_to_test_http2
Authors: windealli
Summary: curl是常用的http测试工具，它能模拟http客户端发送http请求，与http服务器进行通信。通过配置，curl也可以用来测试http2.

curl是常用的http测试工具，它能模拟http客户端发送http请求，与http服务器进行通信。

curl 支持指定协议与服务端进行通信。

```
windeal@ubuntu:src$ curl --help | grep http
-0, --http1.0 Use HTTP 1.0 (H)
--http1.1 Use HTTP 1.1 (H)
--http2 Use HTTP 2 (H)
windeal@ubuntu:src$
```

现在许多http服务器都升级到了http2，我们尝试用curl 访问http2的服务器
```
windeal@ubuntu:src$ curl -I --http2 nghttp2.org
curl: (1) Unsupported protocol
windeal@ubuntu:src$
```
发现curl本身并不支持http2协议。（curl只是提供了use http2的接口，但本身不支持http2协议）

curl可以通过第三方的http2库（nghttp2）来实现对http2的支持。

## 安装nghttp2库
https://github.com/nghttp2/nghttp2/releases 下载nghttp2，并编译安装。

### 安装编译工具
```
sudo apt-get install git g++ make binutils autoconf automake autotools-dev libtool pkg-config \
  zlib1g-dev libcunit1-dev libssl-dev libxml2-dev libev-dev libevent-dev libjansson-dev \
  libjemalloc-dev cython python3-dev python-setuptools
```

### 安装nghttp2
```
$ wget https://github.com/nghttp2/nghttp2/releases/download/vX.Y.Z/nghttp2-X.Y.Z.tar.bz2
$ tar xf nghttp2-X.Y.Z.tar.bz2
$ cd nghttp2-X.Y.Z
$ ./configure
$ make
$ make install
```
如果你下载的是source code，则根目录下并没有configure文件，需要通过下面步骤生成
```
$ autoreconf -i
$ automake
$ autoconf
```
如果有其它编译问题，可以查看REAME.rst文件。

## 升级curl
```
windeal@ubuntu:opt$ wget https://curl.haxx.se/download/curl-7.54.0.tar.bz2
windeal@ubuntu:opt$ tar -jvxf curl-7.54.0.tar.bz2
windeal@ubuntu:opt$ cd curl-7.54.0/
windeal@ubuntu:curl-7.54.0$ ./configure --with-nghttp2=/usr/local --with-ssl
windeal@ubuntu:curl-7.54.0$ make
windeal@ubuntu:curl-7.54.0$ sudo make install
windeal@ubuntu: sudo echo '/usr/local/lib' > /etc/ld.so.conf.d/local.conf
windeal@ubuntu: sudo ldconfig
```
顺便贴上./configure的结果，一遍大家遇到问题时做参考:
```
curl version: 7.54.0
Host setup: x86_64-pc-linux-gnu
Install prefix: /usr/local
Compiler: gcc
SSL support: enabled (OpenSSL)
SSH support: no (--with-libssh2)
zlib support: enabled
GSS-API support: no (--with-gssapi)
TLS-SRP support: enabled
resolver: default (--enable-ares / --enable-threaded-resolver)
IPv6 support: enabled
Unix sockets support: enabled
IDN support: no (--with-{libidn2,winidn})
Build libcurl: Shared=yes, Static=yes
Built-in manual: enabled
--libcurl option: enabled (--disable-libcurl-option)
Verbose errors: enabled (--disable-verbose)
SSPI support: no (--enable-sspi)
ca cert bundle: /etc/ssl/certs/ca-certificates.crt
ca cert path: no
ca fallback: no
LDAP support: no (--enable-ldap / --with-ldap-lib / --with-lber-lib)
LDAPS support: no (--enable-ldaps)
RTSP support: enabled
RTMP support: no (--with-librtmp)
metalink support: no (--with-libmetalink)
PSL support: no (libpsl not found)
HTTP2 support: enabled (nghttp2)
Protocols: DICT FILE FTP FTPS GOPHER HTTP HTTPS IMAP IMAPS POP3 POP3S RTSP SMB SMBS SMTP SMTPS TELNET TFTP
```
## 测试
```
windeal@ubuntu:curl-7.54.0$ curl -I --http2 nghttp2.org
HTTP/1.1 101 Switching Protocols
Connection: Upgrade
Upgrade: h2c

HTTP/2 200
date: Tue, 18 Jul 2017 16:12:14 GMT
content-type: text/html
last-modified: Sun, 02 Jul 2017 08:58:08 GMT
etag: "5958b5a0-19e1"
accept-ranges: bytes
content-length: 6625
x-backend-header-rtt: 0.001355
server: nghttpx
via: 2 nghttpx
x-frame-options: SAMEORIGIN
x-xss-protection: 1; mode=block
x-content-type-options: nosniff
```
**第一次测试其实是失败了，后面发现是curl没有真正更新， 系统的curl还是旧的版本 **
具体原因还不清楚，我直接 `cp curl-7.54.0/src/curl /usr/bin/`