from gattino import Gattino, ExtBase, GattinoEvent
import redis


class Gattino_MQ(ExtBase):
    def get_mq(app: Gattino):
        for item in app.ext:
            if isinstance(item, Gattino_MQ):
                return item
        return None
    conf_key = "gattino_mq"
    redis_url = None
    redis_h = None
    group = None
    expire_time = 0
    heart_beat = 0
    last_heart_beat = 0
    interval = 0
    last_interval = 0
    mq_key = None

    mq_handle = None

    def __init__(self, app: Gattino):
        super(Gattino_MQ, self).__init__(app)
        self.bind_event(GattinoEvent.EVENT_START, self.start)
        self.bind_event(GattinoEvent.EVENT_TICK, self.run)
        self.bind_event(GattinoEvent.EVENT_EXIT, self.stop)

    def load_conf(self):
        conf_dic = dict(self.app.cfg.items(self.conf_key))
        self.redis_url = conf_dic["redis_url"]
        self.group = conf_dic["group"] if "group" in conf_dic else "test"
        self.expire_time = int(conf_dic["expire_time"])
        self.heart_beat = float(conf_dic["heart_beat"])
        self.mq_key = conf_dic["mq_key"]
        self.interval = float(
            conf_dic["interval"]) if "interval" in conf_dic else 0
        return conf_dic

    def send_hb(self):
        self.redis_h.set(
            f"{self.conf_key}:{self.group}:{self.app.appid}", "online", ex=self.expire_time)

    def read_mq(self):
        value = self.redis_h.rpop(self.mq_key)
        if value:
            self.mq_handle(value)

    def bind_msg_handle(self, handle):
        self.mq_handle = handle

    def start(self, params):
        print("mq-start")
        print(self.redis_url)
        print(self.group)
        self.redis_h = redis.Redis.from_url(
            self.redis_url, decode_responses=True)
        self.send_hb()

    def stop(self, params):
        print("mq-stop")
        self.redis_h.delete(
            f"{self.conf_key}:{self.group}:{self.app.appid}")

    def run(self, ts):
        # 发送心跳
        if ts-self.last_heart_beat > self.heart_beat:
            self.last_heart_beat = ts
            self.send_hb()
        # 读消息队列
        if ts-self.last_interval > self.interval:
            self.last_interval = ts
            self.read_mq()
