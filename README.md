## 说明
> 代码由网络收集、ai回答、整理后修改而成，出自哪位原作者已经无从得知    
> 于 2024.11.28 测试通过，可以正常 签到、推送 通知   
> 由于github的CRON表达式会存在延迟执行问题（延迟1小时甚至更久，非时区问题）  
> 所以建议使用第三方支持 CRON表达式 或 定时执行 的平台使用webhook方式触发工作流的运行。   
> 例如 `Cloudflare Workers`  `WPS AirScript`


## 特点 
* 支持多账号
* 支持 手动触发 & webhook触发
* 支持 企业微信机器人通知


## 使用方法  

首先Fork本仓库，然后再点击   
仓库的 `Settings` - `Secrets and variables` - `Actions` - `New repository secret` 绿色按钮  创建以下三个 secret密钥   

`USERNAME` `PASSWORD` `WEBHOOK` 

| 变量名 | 单账户 | 多账户 | 备注 |
| :---------: | :---------: | :---------: | :---------: |
| USERNAME | 15000000000 | 15000000000,13000000000 | 多账号用 `，` 隔开 （*支持中文逗号） |
| PASSWORD | abc123 | abc123，def456 | 多账号用 `，` 隔开 （*支持中文逗号） |
| WEBHOOK | https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx  |  | 企业微信群聊机器人的webhook地址 |
#### 账号  
Name*  填入 `USERNAME`    
Secret* 填入 账号   
* 单账号Secret值   
例如 手机号 `15000000000`  
* 多账号Secret 值  
例如 `15000000000,13000000000`  用 `，` 隔开 （*支持中文逗号） 

#### 密码  
Name*  填入 `PASSWORD`    
Secret* 填入 密码   
* 单账号Secret值   
例如 `abc123`  
* 多账号Secret值   
* 例如 `abc123,def456`  用 `，` 隔开 （*支持中文逗号）    


#### 企业微信机器人信息通知  
Name*  填入 `WEBHOOK` 
Secret* 填入 群聊机器人的webhook地址   
例如 `https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx`   

#### 此时已经可以使用手动触发的方式，运行actions的工作流了。接下来启用 webhook触发工作流 的方法   
点击本仓库的 `Settings` - `Webhooks`  
   
   
## webhook触发工作流  
#### Payload URL *   
填写 `https://api.github.com/repos/拥有者名/仓库名/dispatches`   
#### Content type *   
修改成 `application/json`   

默认 `Enable SSL verification` 不用管   

往下拉，在 *`Which events would you like to trigger this webhook?`* 中，选择 `Let me select individual events.`   
然后勾选 `Workflow runs`  其他不用勾选，点 `Update webhook`   

接下来创建用于 webhook 的 token   
`右上角头像` - `Settings` - `Developer settings` - `Personal access tokens` - `Tokens (classic)`   

点击右上角的 `Generate new token` 下拉框，选 `Generate new token (classic)`    

Note 随便填    
`Expiration` 选 `No expiration`   
然后往下拉 勾选 `workflow`  其它不用选择往下拉，按 `Generate token` 绿色按钮，会显示一段ghp_开头的 token（例如：ghp_xxxxxxxxxxxxxxxxxx）需要保存好，只显示一次   


最后可以使用post请求，webhook触发工作流   
```bash
curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer ghp_xxxxxxxxxxxxxxxxxx" \
  https://api.github.com/repos/拥有者/仓库名/dispatches \
  -d '{"event_type":"sign-in"}'
```

## All Done!!

















