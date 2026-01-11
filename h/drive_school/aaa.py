# fix_simple.py
import sqlite3

# 直接修改数据库文件中的字符串（暴力方法）
with open('初始数据库.db', 'rb') as f:
    data = f.read()

# 把二进制中的中文字符替换
# '运行' 的UTF-8编码是 \xe8\xbf\x90\xe8\xa1\x8c
# '执行' 的UTF-8编码是 \xe6\x89\xa7\xe8\xa1\x8c
data = data.replace(b'\xe8\xbf\x90\xe8\xa1\x8c', b'\xe6\x89\xa7\xe8\xa1\x8c')  # 运行→执行

# '过滤器' 的UTF-8编码是 \xe8\xbf\x87\xe6\xbb\xa4\xe5\x99\xa8  
# '检索' 的UTF-8编码是 \xe6\xa3\x80\xe7\xb4\xa2
data = data.replace(b'\xe8\xbf\x87\xe6\xbb\xa4\xe5\x99\xa8', b'\xe6\xa3\x80\xe7\xb4\xa2')  # 过滤器→检索

with open('初始数据库_修复后.db', 'wb') as f:
    f.write(data)

print("✅ 新数据库已生成：初始数据库_修复后.db")