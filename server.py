#!/usr/bin/env python3
"""
心知天气 MCP 服务器 - 魔搭社区版本
使用标准 MCP 协议提供天气查询服务
"""

import os
import json
import time
import hmac
import hashlib
import base64
from urllib.parse import quote
from mcp import Server, types
import mcp
import asyncio
import aiohttp
from typing import Optional

# 创建MCP服务器实例
app = Server("xinzhi-weather")

class WeatherConfig:
    """配置类"""
    def __init__(self):
        self.default_location = os.getenv("DEFAULT_LOCATION", "yulin")
        self.timeout = int(os.getenv("TIMEOUT", "10"))

config = WeatherConfig()

def generate_signature(params: dict, private_key: str) -> tuple:
    """生成心知天气API签名"""
    sorted_params = sorted(params.items())
    param_str = '&'.join([f"{k}={v}" for k, v in sorted_params])
    
    hmac_obj = hmac.new(
        private_key.encode('utf-8'), 
        param_str.encode('utf-8'), 
        hashlib.sha1
    )
    signature = quote(base64.b64encode(hmac_obj.digest()).decode('utf-8'))
    
    return signature, param_str

async def fetch_weather_data(location: str, public_key: str, private_key: str) -> dict:
    """获取天气数据"""
    try:
        timestamp = str(int(time.time()))
        base_params = {
            'ts': timestamp,
            'ttl': '1800',
            'uid': public_key
        }
        
        signature, param_str = generate_signature(base_params, private_key)
        
        request_params = base_params.copy()
        request_params['sig'] = signature
        request_params['location'] = location
        request_params['language'] = 'zh-Hans'
        request_params['unit'] = 'c'
        
        url = "https://api.seniverse.com/v3/weather/now.json"
        
        timeout = aiohttp.ClientTimeout(total=config.timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, params=request_params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    return {"error": f"API请求失败: {response.status}"}
                    
    except asyncio.TimeoutError:
        return {"error": "请求超时"}
    except Exception as e:
        return {"error": f"请求异常: {str(e)}"}

@app.list_tools()
async def handle_list_tools() -> list[types.Tool]:
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
                        "description": "城市名称，如：beijing、shanghai、yulin",
                        "default": config.default_location
                    },
                    "public_key": {
                        "type": "string", 
                        "description": "心知天气公钥",
                    },
                    "private_key": {
                        "type": "string",
                        "description": "心知天气私钥",
                    }
                },
                "required": ["public_key", "private_key"]
            }
        )
    ]

@app.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """处理工具调用"""
    if name == "get_weather":
        location = arguments.get("location", config.default_location)
        public_key = arguments.get("public_key", "")
        private_key = arguments.get("private_key", "")
        
        if not public_key or not private_key:
            return [types.TextContent(
                type="text",
                text="错误：请提供心知天气的公钥和私钥"
            )]
        
        result = await fetch_weather_data(location, public_key, private_key)
        
        if "error" in result:
            return [types.TextContent(
                type="text",
                text=f"天气查询失败：{result['error']}"
            )]
        
        if "results" in result and result["results"]:
            weather_info = result["results"][0]
            location_name = weather_info["location"]["name"]
            weather_now = weather_info["now"]
            last_update = weather_info["last_update"]
            
            response_text = f"""{location_name} 实时天气信息：

地点：{location_name}
温度：{weather_now['temperature']}°C
天气：{weather_now['text']}
更新：{last_update}

数据来源：心知天气 API"""
            
            return [types.TextContent(type="text", text=response_text)]
        else:
            return [types.TextContent(
                type="text", 
                text=f"未找到城市 '{location}' 的天气数据"
            )]
    
    return [types.TextContent(type="text", text=f"未知工具: {name}")]

async def main():
    """主函数"""
    # 运行MCP服务器
    async with mcp.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream, 
            write_stream,
            mcp.InitializationOptions(
                server_name="xinzhi-weather",
                server_version="1.0.0"
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
