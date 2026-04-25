#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
密码管理脚本
用于生成加密后的密码并验证
"""

import hashlib
import json
import os

PASSWORD_FILE = 'password.json'

class PasswordManager:
    def __init__(self):
        self.password_file = PASSWORD_FILE
        self.load_password()
    
    def load_password(self):
        if os.path.exists(self.password_file):
            with open(self.password_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
        else:
            self.data = {}
    
    def save_password(self):
        with open(self.password_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def set_password(self, password):
        """设置密码并加密存储"""
        hashed = self.hash_password(password)
        self.data['password_hash'] = hashed
        self.save_password()
        print("密码设置成功！")
    
    def hash_password(self, password):
        """加密密码"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def verify_password(self, password):
        """验证密码"""
        if 'password_hash' not in self.data:
            return False
        hashed = self.hash_password(password)
        return hashed == self.data['password_hash']
    
    def generate_token(self):
        """生成访问令牌"""
        import secrets
        token = secrets.token_hex(16)
        self.data['access_token'] = token
        self.save_password()
        return token
    
    def verify_token(self, token):
        """验证访问令牌"""
        return self.data.get('access_token') == token

def main():
    pm = PasswordManager()
    
    print("密码管理工具")
    print("1. 设置密码")
    print("2. 验证密码")
    print("3. 生成访问令牌")
    print("4. 退出")
    
    while True:
        choice = input("请选择操作: ")
        
        if choice == '1':
            password = input("请输入新密码: ")
            pm.set_password(password)
        elif choice == '2':
            password = input("请输入密码: ")
            if pm.verify_password(password):
                print("密码正确！")
                print(f"访问令牌: {pm.generate_token()}")
            else:
                print("密码错误！")
        elif choice == '3':
            token = pm.generate_token()
            print(f"新访问令牌: {token}")
        elif choice == '4':
            break
        else:
            print("无效选择，请重新输入。")

if __name__ == "__main__":
    main()