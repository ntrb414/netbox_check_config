import sys

# 强制将 NetBox 源码目录加入路径，防止 Gunicorn 找不到顶层包
# (保留此段代码以确保服务能正常启动)
NETBOX_ROOT = '/opt/netbox-4.4.8/netbox'
if NETBOX_ROOT not in sys.path:
    sys.path.insert(0, NETBOX_ROOT)

try:
    from netbox.plugins import PluginConfig
except ImportError:
    from extras.plugins import PluginConfig

class ViewConfigConfig(PluginConfig):
    name = 'netbox_view_config'
    verbose_name = '设备配置查看器'
    version = '0.1'
    base_url = 'view-config'
    default_settings = {
        'USERNAME': 'admin',
        'PASSWORD': 'password',
    }

config = ViewConfigConfig
