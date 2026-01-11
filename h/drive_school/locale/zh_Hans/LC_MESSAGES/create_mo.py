#!/usr/bin/env python
"""
创建 django.mo 文件
"""
import struct
import os

# 创建目录
os.makedirs('locale/zh_Hans/LC_MESSAGES', exist_ok=True)

# .mo 文件的二进制数据（简化的只包含3个翻译）
# 这是一个最小化的 .mo 文件结构
mo_data = (
    # Magic number (0x950412de)
    b'\xde\x12\x04\x95'
    # Revision (0)
    b'\x00\x00\x00\x00'
    # Number of strings (3)
    b'\x03\x00\x00\x00'
    # Offset of original strings table
    b'\x20\x00\x00\x00'
    # Offset of translation strings table
    b'\x48\x00\x00\x00'
    # Hash table size (0)
    b'\x00\x00\x00\x00'
    # Offset of hash table (0)
    b'\x00\x00\x00\x00'
    
    # Original strings table
    # String 1: "Run"
    b'\x00\x00\x00\x00'  # length
    b'\x0c\x00\x00\x00'  # offset: 12
    # String 2: "Filter"
    b'\x06\x00\x00\x00'  # length
    b'\x10\x00\x00\x00'  # offset: 16
    # String 3: "Action:"
    b'\x07\x00\x00\x00'  # length
    b'\x1a\x00\x00\x00'  # offset: 26
    
    # Translation strings table
    # Translation 1: "执行"
    b'\x02\x00\x00\x00'  # length
    b'\x24\x00\x00\x00'  # offset: 36
    # Translation 2: "检索"
    b'\x02\x00\x00\x00'  # length
    b'\x2a\x00\x00\x00'  # offset: 42
    # Translation 3: "" (empty string)
    b'\x00\x00\x00\x00'  # length
    b'\x30\x00\x00\x00'  # offset: 48
    
    # Original strings
    b'Run\x00'
    b'Filter\x00'
    b'Action:\x00'
    
    # Translation strings
    b'\xe6\x89\xa7\xe8\xa1\x8c\x00'  # "执行" in UTF-8
    b'\xe6\xa3\x80\xe7\xb4\xa2\x00'  # "检索" in UTF-8
    b'\x00'  # Empty string
)

# 写入文件
with open('locale/zh_Hans/LC_MESSAGES/django.mo', 'wb') as f:
    f.write(mo_data)

print("django.mo 文件已创建")