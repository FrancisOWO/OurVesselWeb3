# OurVesselWeb3
船视宝（myvessel）Web3.0 版

## 项目配置与运行

### 注意事项

本项目的运行依赖于【百度地图】与【船视宝】的 API 接口，需要使用相应的**【密钥】和 【Token】**

请在 **app/utils/config.py** 中进行相关配置：

**1）ak**

【百度地图】开发者密钥，需要在 [**百度地图开放平台**](https://lbsyun.baidu.com/) 的控制台进行开发者认证才可获得

**2）HEADER_AUTHORIZATION**

登录[**【船视宝】网页端**](https://www.myvessel.cn/auth/login) 后，发送请求的 **Header 中的 Authorization** 参数，**【一天后失效，需再次更新】**

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

**使用下面的账号密码：**

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

**4）app/utils/**

项目依赖的 API 接口【梧桐链，船视宝】和 配置参数

**5）app/app_account/**

account 模块目录，用户管理相关功能

**6）app/app_carbon/**

carbon 模块目录，碳排放、碳交易相关功能

**7）app/app_demo/**

demo 模块目录，项目运行示例

**8）app/app_map/**

map 模块目录，地图相关功能

### 文件说明

**1）app.py**

运行该 py 来**启动 flask 项目**，在该文件中设置 ip 和 端口号

**2）config.py**

数据库配置，本项目使用 SQLite 数据库

**3）db_create.py**

运行该 py 来新建数据库（app.db），数据库表结构没有改动就**不用运行**该 py

