try:
    from netbox.plugins import PluginTemplateExtension
except ImportError:
    try:
        from extras.plugins import PluginTemplateExtension
    except ImportError:
        raise

class DeviceConfigButton(PluginTemplateExtension):
    model = 'dcim.device'

    def buttons(self):
        # 兼容 NetBox 4.x (object) 和旧版本 (record)
        obj = self.context.get('object') or self.context.get('record')
        
        # 避开直接访问 primary_ip 属性，直接尝试获取底层的 ip4 或 ip6 对象
        # getattr 在对象没有该属性时会返回 None，不会报错
        ip_obj = getattr(obj, 'primary_ip4', None) or getattr(obj, 'primary_ip6', None)
        
        # 只有当成功获取到管理 IP 对象时，才显示按钮
        if ip_obj:
            return self.render('netbox_view_config/inc/config_button.html', {
                'device': obj,
            })
        return ""

template_extensions = [DeviceConfigButton]
