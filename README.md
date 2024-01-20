# E5_Subscription_AutoActive

基于 HTTP 自动调用 OneDrive 相关 API 请求,模拟开发者活动以续订微软 E5 开发者账号

## 使用说明

在配置文件 config/config.ini 中指定相关程序参数后,点击 /bin/E5KeepActive.exe 文件运行程序.

首次运行会弹出登录对话框，按步骤登录即可.

程序运行正常会在当前登录账号的 OneDrive 网盘上生成 E5KeepActive/E5KeepActive.log 文件(记录了上次调用api的时间).

本地 api 调用 log 在 根目录 E5KeepActive.log 文件中.

本地程序执行错误 log 在 根目录 Error.log 文件中.

### 1. config/config.ini 参数说明

    1.基础配置
        # 是否随系统一起启动，[True or False]
        start_with_system = True

        # API调用时间间隔范围(两端包含), 单位：分钟
        call_func_period = [20,60]
        
        # E5KeepActive 程序运行记录 log 的缓存大小, 单位: MB
        # 可选范围 [0, 250]
        log_size = 10

    2.用户信息(包含的信息来自于你在 Microsoft Entra 管理中心上注册的应用，如若不清楚可自行百度/Google)
        # 客户端ID (Application (client) ID)
        client_id = xxxxxx

        # 客户端密码 (client_value)
        client_secret = xxxxxx

### 2. server_config.json 参数说明
    "SERVER_NAME": "localhost:2233"
    服务名称其实是重定向链接中指定的端口和域名,强烈建议应用的重定向链接配置为: http://localhost:2233/GetAuthorizationCode
    若您的重定向 uri 和 http://localhost:2233/GetAuthorizationCode 保持一致,则此项不需要修改.
### 3. 应用权限说明

    应用的权限组: ["Files.ReadWrite.All", "offline_access"]
        Files.ReadWrite.All 用户文件读写权限
        offline_access      保留允许过的权限
    说明:目前调测阶段文件读写权限较高,建议使用不常用子账号登录应用,以免引起不必要的误会:)

### 4. 应用详细调用API列表
    todo

### 5. one more thing
    微软 Onedrive 客户端实属拉跨,不能指定同步文件夹,不能控制同步方向,不能配置同步计划,不能过滤文件,不能加密文件...
    有意做一个 OneDrive 的第三方客户端,敬请期待.
