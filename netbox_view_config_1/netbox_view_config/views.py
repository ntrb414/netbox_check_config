import os
from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from dcim.models import Device
from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from netmiko import ConnectHandler

class DeviceConfigView(PermissionRequiredMixin, View):
    permission_required = 'dcim.view_device'

    def get(self, request, pk):
        device = Device.objects.get(pk=pk)
        ip_obj = device.primary_ip4 or device.primary_ip6
        ip = str(ip_obj.address.ip) if ip_obj else None
        
        return render(request, 'netbox_view_config/device_config.html', {
            'device': device,
            'device_ip': ip,
            'show_form': True,
        })

    def post(self, request, pk):
        device = Device.objects.get(pk=pk)
        
        # 获取管理IP
        ip_obj = device.primary_ip4 or device.primary_ip6
        if not ip_obj:
            return render(request, 'netbox_view_config/device_config.html', {
                'device': device,
                'error': "设备没有管理IP"
            })
            
        ip = str(ip_obj.address.ip)
        
        # 获取表单提交的认证信息
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # 识别设备驱动
        platform_slug = device.platform.slug if device.platform else 'generic'
        driver_map = {
            'cisco-ios': 'cisco_ios',
            'cisco-xe': 'cisco_ios',
            'cisco-xr': 'cisco_xr',
            'huawei': 'huawei',
            'huawei-vrp': 'huawei',
            'hp-comware': 'hp_comware',
            'h3c': 'hp_comware',
            'juniper-junos': 'juniper_junos',
            'arista-eos': 'arista_eos',
            'vyos': 'vyos',
        }
        
        device_type = driver_map.get(platform_slug)
        if not device_type:
            if 'cisco' in platform_slug:
                device_type = 'cisco_ios'
            elif 'huawei' in platform_slug:
                device_type = 'huawei'
            elif 'hp' in platform_slug or 'h3c' in platform_slug:
                device_type = 'hp_comware'
            else:
                device_type = 'generic_termserver'

        connection_params = {
            'device_type': device_type,
            'host': ip,
            'username': username,
            'password': password,
            'timeout': 15,  # 稍微增加超时时间
        }

        try:
            if not username or not password:
                raise ValueError("必须填写 SSH 用户名和密码")
                
            with ConnectHandler(**connection_params) as net_connect:
                if 'huawei' in device_type or 'hp' in device_type:
                    config_output = net_connect.send_command("display current-configuration")
                else:
                    config_output = net_connect.send_command("show running-config")
        except Exception as e:
            config_output = (
                f"连接失败详情:\n"
                f"------------------\n"
                f"- 目标IP: {ip}\n"
                f"- 识别驱动: {device_type} (基于平台: {platform_slug})\n"
                f"- 尝试账号: {username}\n"
                f"- 错误信息: {str(e)}\n\n"
                f"请检查:\n"
                f"1. 账号密码是否输入正确\n"
                f"2. 设备的 'Platform' 字段是否正确设置\n"
                f"3. 网络是否允许 SSH 连接"
)

        return render(request, 'netbox_view_config/device_config.html', {
            'device': device,
            'device_ip': ip,
            'config': config_output,
            'show_form': False,
            'username': username, # 回显用户名
        })


class DeviceConfigAPIView(PermissionRequiredMixin, View):
    permission_required = 'dcim.view_device'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, pk):
        device = Device.objects.get(pk=pk)
        
        # 构建配置文件路径 /opt/dir1/file1
        # dir1 和 file1 作为占位符，可以根据需要修改
        config_dir = 'dir1'  # 占位符，后续可修改
        config_file = 'file1'  # 占位符，后续可修改
        config_path = f'/opt/{config_dir}/{config_file}'
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config_content = f.read()
                return JsonResponse({
                    'success': True,
                    'config': config_content,
                    'device_name': device.name,
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'配置文件不存在: {config_path}'
                })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'读取配置文件失败: {str(e)}'
            })
