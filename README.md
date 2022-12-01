# OurVesselWeb3
船视宝（myvessel）Web3.0 版

## 项目配置与运行

### 环境配置

**// 1）打开 Anaconda 命令行，新建并激活虚拟环境（Python 3.8.3）**

conda create -n flask python==3.8.3

conda activate flask

**// 2）切换到项目顶层目录（本文件所在目录，也是 req.txt 所在目录），安装依赖**

pip install -r req.txt

### 运行

// 在 flask 虚拟环境中，切换到项目顶层目录（本文件所在目录，也是 app.py 所在目录

// **0）如果没有**数据库文件 app.db 或者 **需要改动数据库结构**，需要先运行 db_create.py ！！！

// python  db_create.py

// **1）运行 app.py**，启动 flask 项目

python app.py

### 登录

登录注册还没做，**用下面的账号密码**：

账号：test12345

密码：test12345

## 项目结构

### 目录说明

**1）app/**

其中包含 static，templates 和 各模块目录

**2）app/static/**

css，images，js，plugins

**3）app/templates/**

各模块**公用的** html

**4）app/app_account/**

account 模块目录

**5）app/app_demo/**

demo 模块目录

### 文件说明

**1）app.py**

运行该 py 来**启动 flask 项目**，在该文件中设置 ip 和 端口号

**2）config.py**

数据库配置，本项目使用 SQLite 数据库

**3）db_create.py**

运行该 py 来新建数据库（app.db），数据库表结构没有改动就**不用运行**该 py

