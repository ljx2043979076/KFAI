# -*- coding: utf-8 -*-
"""
修复 core.py 并简化验证逻辑的脚本
只修改关键验证入口点，最小化改动
"""
import re

# 读取原始文件
with open('core.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 备份原文件
with open('core.py.backup', 'w', encoding='utf-8') as f:
    f.write(content)

print("已备份原文件到 core.py.backup")

# 策略：使用正则表达式找到并替换关键方法

# 1. 替换 start_verify_init 方法
start_verify_pattern = r'(    def start_verify_init\(self\):.*?)(    def )'
start_verify_replacement = r'''    def start_verify_init(self):
        """验证已移除，直接设置为已验证状态"""
        self.verified = True
        print('[验证] 验证已移除，程序已就绪')

\2'''

content = re.sub(start_verify_pattern, start_verify_replacement, content, flags=re.DOTALL)

# 2. 替换 verify 方法
verify_pattern = r'(    def verify\(self\):.*?)(    def _decrypt_encrypted_model)'
verify_replacement = r'''    def verify(self):
        """验证已移除，直接设置为已验证状态"""  
        self.verified = True
        print('[验证] 卡密验证已移除，程序已就绪')
        # 不再需要卡密参数来解密模型
        self._decrypt_encrypted_model(None)

\2'''

content = re.sub(verify_pattern, verify_replacement, content, flags=re.DOTALL)

# 3. 移除 buff imports (如果还存在)
content = re.sub(r'from buff import Buff_Single, Buff_User\n', '', content)

# 4. 在 _change_callback 中移除验证检查
change_callback_pattern = r'(if value == \'start\' and \(not self\.running\):)\s+if not self\.verified:\s+print\(\'验证失败，无法启动推理\'\)\s+return\s+'
change_callback_replacement = r'\1\n                '

content = re.sub(change_callback_pattern, change_callback_replacement, content)

# 写入修复后的文件
with open('core.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("修复完成！")
print("主要更改：")
print("1. 简化 start_verify_init 方法")
print("2. 简化 verify 方法")  
print("3. 移除 buff imports")
print("4. 移除 _change_callback 中的验证检查")
