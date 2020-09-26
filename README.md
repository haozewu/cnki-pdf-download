# paperDownload
因为知网总是拿caj这种论文格式恶心国人，而pdf版中文论文下起来还得去洋大人用的海外版知网去搜，然而使用notability读论文不支持caj，眼看我的速读100篇论文计划光是这番操作就要浪费不少生命，于是抄起键盘花了一天写了这个中文论文下载工具

功能：

- 能够通过关键词进入谷歌学术检索论文

- 能够将硕士、博士论文以pdf的格式下载，而不是专业恶心国人的caj
- 能够自动对论文进行改名



注意！

本程序目前的进度属于Alpha版本，仅具有基础功能，细节完全未修缮。请做好随时出bug的心理准备，同时确保你具有以下条件以进行程序的使用和开发。

- 具有85版本的chrome浏览器（其它版本或者其他浏览器也可以，不过你需要自行下载selenium的webdriver）
- 能够访问谷歌学术
- 处于可用IP登录知网并下载的环境（一般是高校或科研机构）
- 对Python开发有一些了解



使用步骤：

1. 下载这个项目
2. 配置好main文件中谷歌学术使用的代理（第九行附近）
3. 在第20行输入关键词
4. main函数附近可以取消一些print_hi函数的注释以获取更多的搜索结果
5. 运行main.py，运行结束后将会自动打开一个网页，里面是你要的论文标题摘要链接及下载链接，同时会对应生成一个excel（此时你已经可以直接从网页中下载论文，但是下载的文件名字有点毛病）
6. 打开excel，你会发现H列都是0，把你要下载的改成1
7. 打开pdownload.py，第12行改成自己的浏览器默认下载地址
8. 第69行程序等待下载时间可以适当调整，确保等待该时间后能下载完一篇论文（有些地方可能不能下载频率太快，也需要改一改）
9. 运行pdownload.py，等待结束后，你会发现你的paper已经在程序文件夹的paper路径下



不尽如人意之处，如果有人愿意提PR感激不尽：

- main程序打开浏览器那部分跑的太慢了，创建窗口应该挪出来
- 函数和变量命名乱七八糟

- 下载的python程序，不显示窗口就下载不下来，但是使用request处理会默认没有ip登录
- 生成的html丑的一批
- 