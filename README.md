# E5_Subscription_AutoActive

基于 HTTP 自动调用 OneDrive 相关 API 请求,模拟开发者活动以神秘概率续订微软 E5 开发者账号.

**特性：**

    在 windows 本地开机自动运行,不需要服务器. 

## 使用说明

使用本程序主要有两个部分:

    * Microsoft Entra admin center 注册应用 
    * 本应用程序的配置

Microsoft Entra admin center 注册应用操作步骤可参考 [todo: Microsoft Entra admin center 注册应用]()

## 本应用程序的配置

### 运行

在配置文件 config/config.ini 中指定相关程序参数后,点击 /bin/E5KeepActive.exe 文件运行程序.  
首次运行会弹出浏览器登录对话框，按步骤登录即可.  
程序运行正常会在当前登录账号的 OneDrive 网盘根目录下生成 /Apps/E5KeepActive/E5KeepActive.log 文件 (记录了上次调用 api 的时间).  
本地 api 调用 log 在 根目录 E5KeepActive.log 文件中.  
本地程序执行错误 log 在 根目录 Error.log 文件中.

### 参数说明

#### 1. config/config.ini 

1.基础配置

```ini
		# 是否随系统一起启动,可选范围[True or False]
		start_with_system = True
		
		# API调用时间间隔范围(两端包含),单位：分钟
		call_func_period = [20,60]
		
		# E5KeepActive 程序运行记录 log 的缓存大小,单位: MB,可选范围 [0, 250]
		log_size = 10
```

2.用户信息 (包含的信息来自于你在 Microsoft Entra 管理中心上注册的应用,可参考 [todo: Microsoft Entra admin center 注册应用]())

```ini
		# 客户端ID (Application (client) ID)
		client_id = xxxxxx
		
		# 客户端密码 (client secret value,not secret id)
		client_secret = xxxxxx

```

#### 2. config/server_config.json

```json
{
		"SERVER_NAME": "localhost:2233"
}
```

服务名称为重定向链接中指定的 ip 和 端口,强烈建议应用的重定向链接配置为: http://localhost:2233/GetAuthorizationCode

若您的重定向 uri 和 http://localhost:2233/GetAuthorizationCode 保持一致,则此项不需要修改.  
(为避开微软神秘的账户活动遥测,可更改端口值 ex: 2233 --> 6666)

### 其他

#### 应用权限说明

    应用的权限组: ["Files.ReadWrite.All", "offline_access"]
			 Files.ReadWrite.All 用户文件读写权限
			 offline_access      保留允许过的权限
    说明:目前调测阶段文件读写权限较高,建议使用不常用子账号登录应用,以免引起不必要的误会:)

#### 应用详细调用 API 列表

    todo

#### 应用解绑

	todo

#### 挖坑计划

    目前微软 Onedrive 客户端不能指定同步文件夹,不能控制同步方向,不能配置同步计划,不能过滤文件,不能加密文件...
    计划做一个好看实用的 OneDrive 第三方客户端.
