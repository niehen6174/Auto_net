# 自动联网脚本

> 脚本使用的方法是：用了Selenium ，一个用于 Web 应用程序测试的工具。测试直接自动运行在浏览器中，打开网页登录界面，自动输入学号密码进行登录，联网。

## 使用方法

使用该脚本需要安装有Chrome浏览器，并下载相对应版本的`chrome-driver`

1. 查看chrome浏览器版本号
    ![enter description here](https://gitee.com/nie_hen/XSJ_img/raw/master/小书匠/1641453990915.png)
2. 查看对应的版本
 ![enter description here](https://gitee.com/nie_hen/XSJ_img/raw/master/小书匠/1641454363535.png)
    ![enter description here](https://gitee.com/nie_hen/XSJ_img/raw/master/小书匠/1641454372805.png)
 3. `chrome-dirver`下载地址
      [官网](https://chromedriver.chromium.org/downloads)
      [国内仓库](http://chromedriver.storage.googleapis.com/index.html)
      ![enter description here](https://gitee.com/nie_hen/XSJ_img/raw/master/小书匠/1641454543632.png)


下载下来后,将`chromedriver.exe`放入一个能找到的目录（尽量不要带中文路径）即可

4. 把该脚本下载下来。
   1. windows下 可以直接用打包好的exe ，（conf文件也需要下载下来）
   2. linux下需要配置下环境  `pip install selenium schedule` 。在代码前面写入需要的参数，运行即可。

## 界面
![enter description here](https://gitee.com/nie_hen/XSJ_img/raw/master/小书匠/1641721226816.png)



## 需要注意的地方

1. 没有检查密码错误的机制，所以用户名和密码要写正确。

2. 首先要写入用户名、密码以及选择chrome-driver的地址。然后点击自动联网。（需要几秒钟时间）
   连上网之后会有 Success! 的提示，出现报错会显示 Error。

3. 时间间隔建议输入大于5的整数。单位是分钟。是个定时任务，会去检测网络情况，如果网络中断，会执行联网的程序。学校网络是24小时中断一次，如果在网断的时候执行这个程序，那么时间间隔可以设置的长一些，几个小时为单位。

4. check-net 按钮会去检测当前情况下的网络状态。

5. 程序短暂的无反应是在检测网络，当前线程占用，界面会卡住，如果长时间无反应，则是有问题，chrome-driver版本不对 或者路径不对
6. 程序右上角关闭之后，有些情况下进程还在跑（不知道哪的问题），可以在任务管理器里杀死。

