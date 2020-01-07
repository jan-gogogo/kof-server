import json
import subprocess
from subprocess import PIPE
from app.eospy.keys import EOSKey

import urllib3

http = urllib3.PoolManager()

# 使用麒麟测试链
EOS_HOST = 'https://api-kylin.eosasia.one'
# 我们的智能合约账号
CONTRACT = 'kingofighter'
# 构建EOS key
k = EOSKey("你的智能合约私钥地址")


def sign(digest):
    """
    使用指定私钥进行签名
    :param digest: 需要签名的数据
    :return: 签名后数据
    """
    return k.sign(digest)


def index_table(table, lower_bound, limit, index_position):
    """
    构建一个索引查找模式的参数
    :param table: 合约的表名
    :param lower_bound: 查找的起始值
    :param limit: 查找数量
    :param index_position: 索引位置，主键为1
    :return: 索引查找的参数
    """
    return base(CONTRACT, table, CONTRACT, lower_bound, limit, index_position)


def base(contract, table, scope, lower_bound, limit, index_position):
    if index_position == 1:
        return {'code': contract,
                'table': table,
                'json': 'true',
                'limit': limit,
                'lower_bound': lower_bound,
                'scope': scope}
    else:
        return {'code': contract,
                'table': table,
                'json': 'true',
                'limit': limit,
                'lower_bound': lower_bound,
                'scope': scope,
                'key_type': 'i64',
                'index_position': index_position}


def query_table_RPC(args):
    """
    使用RPC方式查询表
    :param args: 查询入参
    :return: 查询结果
    """
    encode_data = json.dumps(args).encode('utf-8')
    r = http.request('POST', EOS_HOST + '/v1/chain/get_table_rows', body=encode_data)
    data = json.loads(r.data.decode('utf-8'))
    return data['rows']


def exec_battle_cmd(game_id, house_seed):
    """
    通过本地安装的cleos客户工具，调用智能合约，进行对战操作
    :param game_id: 游戏id
    :param house_seed: 服务端种子
    :return: 是否执行成功
    """
    cmd = "cleos -u " + EOS_HOST + " push action " + CONTRACT + " battle '[" + str(
        game_id) + ",\"" + house_seed + "\"]' -p " + CONTRACT
    p = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    stdout, stderr = p.communicate()
    exit_code = p.returncode
    return exit_code == 0
