Title: 同步异步与阻塞非阻塞
Date: 2018-08-03 19:00:44
Modified: 2018-08-03 19:00:44
Category: background
Tags: 异步, 同步, 阻塞
Slug: sync_async_nonblock
Authors: windealli
Summary: 同步异步与阻塞非阻塞是开发中经常碰到的概念，但是很多人都没理解清楚，或者混淆了它们的概念。最近看了一些材料，发现以前很多理解都是错的，所以重新整理了一下。


## 同步异步与阻塞非阻塞
标题有点简单粗暴，直接用了本文要介绍的几个概念。本来想取个高大上一点的标题，但是感觉主题不那么明了。

好，废话不多说，进入正题。

如果你是个研发，同步、异步、阻塞、非阻塞（还有IO多路复用）这些概念应该不陌生了。但是很多人却没有真正搞懂他们的含义，甚至经常把他们混淆了。

先上几个**错误**的表达提提神：

1. 非阻塞IO模型是异步IO。
2. IO多路复用模型是异步IO。

第一个表达，“非阻塞IO模型是异步IO” 的说法是错误的，在UNP一书中有介绍，那么“非阻塞IO模型是同步IO模型”正确么？从《Unix网络编程》6.2节中的描述来看，是正确的。但我认为不够准确，或者说容易产生误解。UNP英文版中说的是“blocking, nonblocking, I/O multiplexing, and signal-driven I/O—are all synchronous”， 但UNP的中文版翻译成“非阻塞I/O模型是同步I/O模型”，我觉得翻译成“基于同步I/O的模型”，或者直接说它是同步的更好一点 。

先说下本文的主要观点：

1. **讨论同步、异步、阻塞、非阻塞这些概念的时候，要先确定讨论范围。**
先确定要讨论的是IO模型，还是IO操作，又或是在讨论线程的安全机制。讨论的范围不同，这些概念的含义也会发生变化。
2. **异步和非阻塞的区别主要在于是否需要等待获取对方状态后再返回。**

## IO 操作

关于IO操作，

首先说下阻塞与非阻塞的概念：

IO操作的完成往往是需要一定条件的，比如等待可读、可写的，也就是说IO操作很可能是没办法立即完成的。那么，如果在IO操作没办法立即完成时，不继续往下执行而是等待其完成，则该操作是阻塞的。如果我们不等待，则认为其实非阻塞的。

在Unix网络编程中，可以通过fcntl或者ioctl将socket套接字设置为非阻塞模式，该套接字字上的操作就会编程非阻塞IO操作。

再来讨论下同步与异步的概念：

同步操作和异步操作这样的表达其实也不太贴切，其实在IO操作中，他们更多是用来描述调用在何时返回。在man aio_read是这样描述异步（操作）的：

> The “asynchronous” means that this call returns as soon as the request has been enqueued; the read may or may not have completed when the call returns.

看起来跟非阻塞IO操作的概念没什么不同，其实不然。异步IO操作是：只要把request加入到队列中就返回。和非阻塞IO操作不同的是，异步操作连描述符是否准备好也不需要去检查。也就是说，异步IO操作返回的时候，可能还不知道描述符准备好了没；而非阻塞操作返回时，最少我们可以通过返回值判断其是否处于可读、可写等状态。

同步IO操作和异步IO操作是相对而言的。

从上面的介绍可以得出：

**如果一个IO操作是异步操作，那他一定是非阻塞的。但是如果非阻塞操作却未必是异步IO操作。**

实际上异步IO操作仅有少数API支持（如aio_read，aio_fsync等aio_xxx形式）。我们通常使用的网络IO操作，基本上都是同步IO操作，不管它是阻塞的还是非阻塞的。

## IO模型
关于IO模型，UNP 6.2节 有列举了常见的五中IO模型。

+ 阻塞I/O模型
+ 非阻塞I/O模型
+ I/O多路复用模型
+ 信号驱动I/O模型
+ 异步I/O模型

关于这五种模型各自的含义，UNP中有比较详细的描述了。

这里要注意，讨论的范围是模型，而不是IO操作。

实际上UNP也有明确阐述了：前面四种模型是都是同步，最后一种模型是异步的。不过UNP里面给出的原因我是有点疑问的（望大佬解疑）：

> POSIX defines these two terms as follows:
A synchronous I/O operation causes the requesting process to be blocked until that I/O operation completes.
An asynchronous I/O operation does not cause the requesting process to be blocked.
Using these definitions, the first four I/O models—blocking, nonblocking, I/O multiplexing, and signal-driven I/O—are all synchronous because the actual I/O operation (recvfrom) blocks the process. Only the asynchronous I/O model matches the asynchronous I/O definition.

这里给出的前四种模型是同步的原因是because the actual I/O operation (recvfrom) blocks the process，并且举例了recvfrom。 如果根据前面给出的POSIX定义来看，表述应该是没问题的。关键点就在POSIX里面的定义表述中使用的block不太贴切。跟我前面引用的man aio_read的表述有些诧异。我认为”causes the requesting process to be blocked “中的block和我们理解的阻塞是不一致的。

## 进程同步与线程同步

谈到（并发）服务器编程时，经常会听到进程同步，线程同步等概念。这里的同步和同步IO中的同步是较大区别的。

### 进程同步

临界资源（临界区）： 一次只能允许一个进程使用的共享资源

进程同步：为完成某种任务而建立的多个进程需要协调它们的工作流程，以保证对临界资源的有序访问。确保不会互相干扰。

进程同步的手段就是进程间通信。关于进程间通信APUE等书上都讲得很清楚了，不再累述。

### 线程同步
多线程编程时，经常会提到线程同步，那么什么是线程同步？

线程同步的概念和进程同步有点类似。主要差别在于其“临界资源”不同。

我们说进程是资源分配的基本单位，也就是说多线程会共享一些资源（内存），这些资源就是线程同步的“临界资源”。

线程同步一般是通过加锁保护实现。线程同步需要保证同一块内存同一个时间内只有一个写用户。

## 异步编程
做后台开发的时候，经常还会谈到异步编程。这里异步跟前面的异步IO不是一个维度的概念。

异步编程的概念是比较模糊的。异步编程跟进程同步、线程同步有点关系，或者说异步编程实现进程同步和线程同步的一种编程思想。在编程时，考虑了（实现了）进程同步和线程同步，就可以认为是异步编程。

## 总结
前面根据概念的的讨论范围，分别介绍了与同步、异步、阻塞、非阻塞等相关的概念。其实他们也是有共通点的。

**同步和异步关注的是消息的通信机制。**
异步就是，我告诉你要做什么（request），至于现在能不能做，什么时候做，我并不关心，通知下发了（enqueue）就返回。反之则是同步。

**阻塞和非阻塞关注的是最终结果是否返回了。**
非阻塞就是：我告诉你我要做什么，如果现在能做，那就做完再返回；如果现在还做不了，你也给我个信儿，跟我说这事儿还做不了。