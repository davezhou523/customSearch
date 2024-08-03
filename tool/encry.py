import hashlib
def generate_md5(message):
    md5 = hashlib.md5()  # 创建一个md5对象
    md5.update(message.encode('utf-8'))  # 使用utf-8编码消息
    return md5.hexdigest()  # 返回十六进制的哈希值