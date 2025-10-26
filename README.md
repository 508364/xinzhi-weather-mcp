
# 心知天气 MCP Server

基于心知天气API的Model Context Protocol服务，提供安全、实时的天气查询功能。

## 🌤️ 功能特性

- **实时天气查询**：获取全国400+城市的实时天气数据
- **安全认证**：采用HMAC-SHA1签名验证，保障API安全
- **标准协议**：完全兼容MCP（Model Context Protocol）标准
- **简单易用**：开箱即用，无需复杂配置

## 📦 快速开始

### 前置要求

- Python 3.8+
- 心知天气API账户（https://www.seniverse.com/）

### 安装部署

#### 方法一：魔搭社区一键部署
1. 在魔搭社区MCP创建页面选择"从Github仓库快速创建"
2. 填写本仓库地址：`https://github.com/your-username/xinzhi-weather-mcp`
3. 系统将自动解析并完成基础配置

#### 方法二：手动本地部署

```bash
# 克隆仓库
git clone https://github.com/your-username/xinzhi-weather-mcp.git
cd xinzhi-weather-mcp

# 安装依赖
pip install -r requirements.txt

# 启动服务
python server.py
```

## ⚙️ 配置说明

### 服务配置（魔搭社区）
在创建MCP Server时，在"服务配置"区域使用以下JSON配置：

```json
{
  "mcpServers": {
    "xinzhi-weather": {
      "command": "python",
      "args": ["server.py"],
      "env": {
        "PYTHONPATH": "."
      }
    }
  }
}
```

### 环境变量配置（可选）
| 变量名 | 描述 | 类型 | 必填 | 默认值 |
|-------|------|------|------|--------|
| `DEFAULT_LOCATION` | 默认查询城市 | string | 否 | yulin |

### API密钥配置
用户需要在MCP客户端中配置自己的心知天气API密钥：

```json
{
  "public_key": "您的公钥",
  "private_key": "您的私钥"
}
```

## 🛠️ 使用方法

### 支持的MCP客户端
- Claude Desktop
- Cursor Editor  
- 其他支持MCP协议的客户端

### 工具调用示例
在支持的客户端中调用 `get_weather` 工具：

```json
{
  "location": "beijing",
  "public_key": "your_public_key_here",
  "private_key": "your_private_key_here"
}
```

### 响应示例
```json
{
  "status": "success",
  "data": {
    "location": {
      "name": "北京",
      "country": "中国",
      "path": "北京,北京,中国"
    },
    "weather": {
      "condition": "晴",
      "temperature": "21°C",
      "temp_numeric": 21
    },
    "last_update": "2024-01-20T14:30:00+08:00"
  }
}
```

## 🔧 API密钥申请

1. 访问https://www.seniverse.com/
2. 注册账号并完成实名认证
3. 进入控制台创建新应用
4. 获取公钥(uid)和私钥(key)

## 📊 支持的城市

支持全国所有地级市及以上城市，使用拼音或中文名称均可：
- 北京 / beijing
- 上海 / shanghai  
- 广州 / guangzhou
- 深圳 / shenzhen
- 玉林 / yulin

## 🐛 故障排除

### 常见问题

**Q: 返回"签名验证失败"**
A: 检查公钥私钥是否正确，确保时间同步

**Q: 返回"城市不存在"**  
A: 使用标准的城市拼音名称，如"beijing"而非"beijing-shi"

**Q: 服务启动失败**
A: 检查Python版本和依赖安装，确保端口6000未被占用

### 日志查看
服务运行日志会输出到控制台，包含详细的错误信息用于调试。

## 📄 许可证

MIT License
