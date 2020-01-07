import time
import urllib3
import random
import hashlib
import app.service.eos.eos_service as EOS
import app.redis_service as REDIS

http = urllib3.PoolManager()


def generate_house_seed():
    """
    生成服务端种子
    格式：当前时间戳 + 0-9999999的随机数，再算出哈希值
    :return:
    """
    ms = int(round(time.time() * 1000))
    rd = random.randint(0, 9999999)
    seed = sha256(str(ms) + str(rd))
    return seed


def get_expire_timestamp():
    """
    过期时间，当前时间戳 + 600秒
    :return:
    """
    return int(time.time()) + 600


def sha256(text):
    """
    对内容进行sha256哈希计算
    :param text: 原内容
    :return: 内容哈希值
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def get_seed():
    """
    提供给客户端玩家的种子相关数据
    :return: 包含服务端种子哈希、有效时间、签名数据
    """
    # 服务端种子；重要数据，不可泄露
    house_seed = generate_house_seed()
    # 服务端种子哈希，返回给客户端玩家
    house_seed_hash = sha256(house_seed)
    # 本次签名数据过期时间，返回给客户端玩家
    expire_timestamp = get_expire_timestamp()
    # 本次签名数据，格式：服务端种子哈希+过期时间戳
    sig_data = house_seed_hash + str(expire_timestamp)
    digest = sha256(sig_data)
    sig = EOS.sign(digest)

    for_client_m = {"house_seed_hash": house_seed_hash,
                    "expire_timestamp": expire_timestamp,
                    "sig": sig}
    for_server_m = {"house_seed": house_seed,
                    "house_seed_hash": house_seed_hash,
                    "expire_timestamp": expire_timestamp,
                    "sig": sig}
    REDIS.set(house_seed_hash, for_server_m)
    return for_client_m


def battle_timer():
    """
    轮询合约的games表，通过索引找出需要处理的游戏（status==1）
    以house_seed_hash作为缓存key，从缓存中取出需要处理的游戏数据
    通过本地安装的cleos客户工具，调用智能合约，进行对战操作
    执行成功后可删除本地缓存
    """
    args = EOS.index_table(table='games', lower_bound=1, limit=100, index_position=3)
    while True:
        rows = EOS.query_table_RPC(args)
        if len(rows) == 0:
            # 没有任何需要处理的数据
            continue

        for r in rows:
            if r['status'] == 1:
                cache_key = r['house_seed_hash']
                cache_obj = REDIS.get(cache_key)
                if cache_obj is not None:
                    # 从缓存中取出游戏数据
                    game = eval(cache_obj)
                    # 调用智能合约
                    exec_r = EOS.exec_battle_cmd(game_id=r['game_id'], house_seed=game['house_seed'])
                    if exec_r is True:
                        # 如果执行成功，清除缓存
                        REDIS.remove(cache_key)

        time.sleep(2)
