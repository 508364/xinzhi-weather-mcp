# 心知天气 MCP 服务

基于心知天气API的Model Context Protocol服务，提供实时天气查询功能。

## 魔搭社区部署说明

### 服务配置
在魔搭社区创建MCP服务时，使用以下配置：

```json
{
  "mcpServers": {
    "xinzhi-weather": {
      "command": "python",
      "args": ["server.py"],
      "env": {
        "PYTHONPATH": ".",
        "XZ_PUBLIC_KEY": "您的心知天气公钥",
        "XZ_PRIVATE_KEY": "您的心知天气私钥", 
        "XZ_DEFAULT_LOCATION": "yulin"
      }
    }
  }
}
```

### 使用方法
在支持MCP的客户端中调用 `get_weather` 工具：

```python
# 示例调用
result = await client.call_tool("get_weather", {
    "location": "beijing",
    "public_key": "您的公钥",
    "private_key": "您的私钥"
})
```

### API密钥申请
1. 访问心知天气官网注册账号
2. 在控制台申请API密钥
3. 获取公钥和私钥
```

## 5. 魔搭社区创建步骤

1. **在GitHub创建仓库**：上传以上4个文件
2. **魔搭社区创建MCP**：
   - 选择"从GitHub导入"
   - 仓库地址：`https://github.com/您的用户名/xinzhi-weather-mcp`
   - 服务配置：使用上面的 `mcp.json` 内容
   - 入口文件：`server.py`
   - Python版本：3.9

3. **部署测试**：魔搭社区会自动安装依赖并启动服务
