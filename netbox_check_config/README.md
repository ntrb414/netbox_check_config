# NetBox Check Config Plugin

这是一个用于 NetBox 的插件，允许用户直接在设备详情页面查看备份的配置文件。

## 功能特点

- 在设备详情页添加“查看配置”按钮。
- 通过弹窗实时读取并显示设备的备份配置文件。
- 支持自定义配置文件存放路径。

## 安装方法

1. 下载或克隆此仓库：
   ```bash
   git clone https://github.com/ntrb414/netbox_check_config.git
   ```

2. 安装插件：
   ```bash
   pip install ./netbox-check-config
   ```

3. 在 NetBox 的 `configuration.py` 中启用插件：
   ```python
   PLUGINS = [
       'netbox_check_config',
   ]
   ```

4. 运行迁移（如果需要）：
   ```bash
   python3 manage.py migrate
   ```

5. 重启 NetBox 服务：
   ```bash
   sudo systemctl restart netbox
   ```

## 配置说明

目前插件默认从 `/opt/dir1/file1` 读取配置文件（可以在 `views.py` 中根据实际需求修改逻辑）。后续版本将支持在后台配置路径模板。

## 使用说明

1. 进入任意设备的详情页面。
2. 点击右上角的“查看配置”按钮。
3. 在弹出的对话框中即可查看该设备的配置内容。
