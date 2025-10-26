#!/usr/bin/env python3
"""
心知天气 MCP 服务器
使用标准 MCP 协议提供天气查询服务
"""

import asyncio
import os
import json
import time
import hmac
import hashlib
import base64
from urllib.parse import quote
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
from pydantic import BaseModel

# 创建MCP服务器实例
server = Server("xinzhi-weather")

class WeatherArgs(BaseModel):
    """天气查询参数"""
    location: str = "yulin"
    public_key: str
    private_key: str

def generate_signature(params, private_key):
    """生成心知天气API签名"""
    sorted_params = sorted(params.items())
    param_str = '&'.join([f"{k}={v}" for k, v in sorted_params])
    
    hmac_obj = hmac.new(private_key.encode('utf-8'), param_str.encode('utf-8'), hashlib.sha1)
    signature = quote(base64.b64encode(hmac_obj.digest()).decode('utf-8'))
    
    return signature, param_str

async def get_weather_data(args: WeatherArgs):
    """获取天气数据"""
    try:
        import aiohttp
        import asyncio
        
        timestamp = str(int(time.time()))
        base_params = {
            'ts': timestamp,
            'ttl': '1800',
            'uid': args.public_key
        }
        
        signature, param_str = generate_signature(base_params, args.private_key)
        
        request_params = base_params.copy()
        request_params['sig'] = signature
        request_params['location'] = args.location
        request_params['language'] = 'zh-Hans'
        request_params['unit'] = 'c'
        
        url = "https://api.seniverse.com/v3/weather/now.json"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=request_params, timeout=10) as response:
                data = await response.json()
                return {"status": "success", "data": data}
                
    except Exception as e:
        return {"status": "error", "message": str(e)}

@server.list_tools()
async def list_tools():
    """列出可用工具"""
    return [
        types.Tool(
            name="get_weather",
            description="查询指定城市的实时天气信息",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "城市名称，如：beijing、shanghai、yulin"
                    },
                    "public_key": {
                        "type": "string", 
                        "description": "心知天气公钥"
                    },
                    "private_key": {
                        "type": "string",
                        "description": "心知天气私钥"
                    }
                },
                "required": ["public_key", "private_key"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """调用工具"""
    if name == "get_weather":
        args = WeatherArgs(**arguments)
        result = await get_weather_data(args)
        
        if result["status"] == "success":
            data = result["data"]
            if 'results' in data and data['results']:
                weather = data['results'][0]['now']
                location = data['results'][0]['location']
                
                return [
                    types.TextContent(
                        type="text",
                        text=f"""{location['name']}当前天气：
- 天气状况：{weather['text']}
- 温度：{weather['temperature']}°C
- 最后更新：{data['results'][0]['last_update']}"""
                    )
                ]
            else:
                return [
                    types.TextContent(
                        type="text", 
                        text="未找到该城市的天气数据"
                    )
                ]
        else:
            return [
                types.TextContent(
                    type="text",
                    text=f"查询失败：{result['message']}"
                )
            ]
    
    raise ValueError(f"未知工具: {name}")

@server.list_resources()
async def list_resources():
    """列出资源（可选）"""
    return []

@server.read_resource()
async def read_resource(uri: str):
    """读取资源（可选）"""
    raise ValueError(f"未知资源: {uri}")

async def main():
    """主函数"""
    # 使用stdio传输运行服务器
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="xinzhi-weather",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities=None
                )
            ),
        )

if __name__ == "__main__":
    asyncio.run(main())
