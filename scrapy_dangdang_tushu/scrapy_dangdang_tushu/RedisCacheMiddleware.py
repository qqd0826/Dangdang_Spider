import pickle
from scrapy import Request, signals
from scrapy.exceptions import NotConfigured
from scrapy_redis import get_redis_from_settings

class RedisCacheMiddleware:
    def __init__(self, settings):
        if not settings.get('REDIS_HOST'):
            raise NotConfigured("Missing REDIS_HOST setting")

        self.redis = get_redis_from_settings(settings)
        self.cache_key_prefix = 'response_cache_'

    @classmethod
    def from_crawler(cls, crawler):
        obj = cls(crawler.settings)
        crawler.signals.connect(obj.spider_opened, signal=signals.spider_opened)
        return obj

    def spider_opened(self, spider):
        self.cache_key_prefix += f"{spider.name}_"

    def process_request(self, request, spider):
        cache_key = self.cache_key_prefix + request.url
        cached_response = self.redis.get(cache_key)

        if cached_response is not None:
            # 解析并返回缓存的响应对象
            response = pickle.loads(cached_response)
            return response

        # 如果没有缓存，则继续处理请求
        return None

    def process_response(self, request, response, spider):
        if response.status == 200:  # 只缓存HTTP 200状态码的响应
            cache_key = self.cache_key_prefix + request.url
            # 将响应对象序列化后存储到Redis
            # 设置过期时间为一小时
            self.redis.setex(cache_key,3600,value=pickle.dumps(response))

        return response

    def process_exception(self, request, exception, spider):
        # 当出现异常时，不执行缓存操作
        pass