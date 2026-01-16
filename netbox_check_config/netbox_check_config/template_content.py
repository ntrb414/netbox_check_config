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
        
        # 显示按钮，不需要检查IP
        return self.render('netbox_view_config/inc/config_button.html', {
            'device': obj,
        })
    
    def right_page(self):
        # 添加弹窗到页面
        obj = self.context.get('object') or self.context.get('record')
        return self.render('netbox_view_config/inc/config_modal.html', {
            'device': obj,
        })

template_extensions = [DeviceConfigButton]
