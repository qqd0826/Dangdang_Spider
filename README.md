# Dangdang_Spider

## 原架构和运行

windows系统默认终端：

```powershell
scrapy crawl ddts
```

### 项目结构
```
Dangdang_Spider
│  └─ scrapy_dangdang_tushu
│     ├─ scrapy.cfg
│     └─ scrapy_dangdang_tushu
│        ├─ items.py
│        ├─ middlewares.py
│        ├─ pipelines.py
│        ├─ RedisCacheMiddleware.py
│        ├─ settings.py
│        ├─ spiders
│        │  ├─ books
│        │  ├─ ddts.py
│        │  └─ __init__.py
│        └─ __init__.py
```

### 功能说明

爬取成功后会将图片以jpg格式保存到books目录下，将商品名、价格、图片URL地址保存到Mysql数据库中


## 数据库
数据库在管道开启时连接，连接自己的本地数据库请修改以下配置

```python
self.conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='ddts')
```

## redis
redis默认配置如下

```python
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
```

