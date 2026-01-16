# NetBox Check Config Plugin

一个用于通过 SSH 连接查看网络设备配置的 NetBox 插件。

## 功能特性

- 🔗 **SSH 连接**: 通过 Netmiko 库安全连接到网络设备
- 🌐 **多厂商支持**: 支持 Cisco、华为、H3C、Juniper、Arista 等主流网络设备
- 🔧 **自动驱动识别**: 根据设备平台自动选择正确的驱动程序
- 🖥️ **Web 界面**: 在 NetBox 设备详情页面直接查看配置
- 📡 **API 接口**: 提供 RESTful API 获取设备配置
- 🔐 **安全认证**: 支持用户名密码认证，权限控制

## 支持的设备平台

| 平台标识 | Netmiko 驱动 | 命令 |
|---------|-------------|------|
| cisco-ios, cisco-xe | cisco_ios | `show running-config` |
| cisco-xr | cisco_xr | `show running-config` |
| huawei, huawei-vrp | huawei | `display current-configuration` |
| hp-comware, h3c | hp_comware | `display current-configuration` |
| juniper-junos | juniper_junos | `show running-config` |
| arista-eos | arista_eos | `show running-config` |
| vyos | vyos | `show running-config` |

## 安装要求

- NetBox 3.x 或 4.x
- Python 3.8+
- netmiko

## 安装步骤

1. **克隆项目**
   ```bash
   git clone https://github.com/ntrb414/netbox_check_config.git
   cd netbox_check_config
   ```

2. **安装插件**
   ```bash
   pip install .
   ```

3. **配置 NetBox**
   
   在 `configuration.py` 中添加插件：
   ```python
   PLUGINS = [
       'netbox_view_config',
   ]
   
   # 可选配置
   PLUGINS_CONFIG = {
       'netbox_view_config': {
           'USERNAME': 'admin',  # 默认用户名
           'PASSWORD': 'password',  # 默认密码
       }
   }
   ```

4. **重启 NetBox 服务**
   ```bash
   sudo systemctl restart netbox
   sudo systemctl restart netbox-rq
   ```

## 使用方法

### Web 界面使用

1. 在 NetBox 中导航到设备详情页面
2. 点击 "查看配置" 按钮
3. 输入 SSH 认证信息（用户名和密码）
4. 点击连接查看设备配置

### API 使用

```bash
# 获取设备配置 API
GET /plugins/view-config/device/{device_id}/config-api/
```

响应示例：
```json
{
  "success": true,
  "config": "device configuration content...",
  "device_name": "router01"
}
```

## 项目结构

```
netbox_check_config/
├── setup.py                    # 安装配置
├── MANIFEST.in                 # 打包配置
├── netbox_check_config/        # 主包目录
│   ├── __init__.py             # 插件配置类
│   ├── views.py                # 视图逻辑
│   ├── urls.py                 # URL 路由
│   ├── template_content.py     # 模板扩展
│   └── templates/              # HTML 模板
│       └── netbox_view_config/
│           ├── device_config.html
│           └── inc/
│               ├── config_button.html
│               └── config_modal.html
└── README.md                   # 项目文档
```

## 权限要求

用户需要具备以下权限才能使用插件：
- `dcim.view_device`: 查看设备信息

## 安全注意事项

1. **网络访问**: 确保 NetBox 服务器能够通过 SSH 访问目标设备
2. **防火墙**: 检查防火墙规则允许 SSH 连接（默认端口 22）
3. **凭据安全**: 建议使用环境变量或 NetBox 密钥管理存储敏感信息
4. **日志记录**: 连接失败信息会记录在 NetBox 日志中

## 故障排除

### 连接失败常见原因

1. **设备 IP 配置**: 确保设备配置了正确的主 IP
2. **平台设置**: 检查设备的 "Platform" 字段是否正确设置
3. **网络连通性**: 确保 NetBox 服务器能访问设备 IP 的 SSH 端口
4. **认证信息**: 验证用户名和密码是否正确

### 调试信息

连接失败时会显示详细信息：
- 目标 IP 地址
- 识别的设备驱动
- 使用的用户名
- 具体错误信息

## 开发与贡献

欢迎提交 Issue 和 Pull Request 来改进这个插件。

### 开发环境设置

1. Fork 项目
2. 创建开发分支
3. 进行修改
4. 提交 Pull Request

## 许可证

本项目采用 MIT 许可证。

## 更新日志

### v0.1 (2025-01-16)
- 初始版本发布
- 支持主流网络设备厂商
- Web 界面和 API 接口
- 自动设备驱动识别

## 联系方式

如有问题或建议，请通过 GitHub Issues 联系。