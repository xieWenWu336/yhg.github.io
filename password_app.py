#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
密码管理脚本和服务器
用于生成加密后的密码并验证，以及提供本地密码验证服务器
"""

import hashlib
import json
import os
import http.server
import socketserver
import traceback
import secrets

PASSWORD_FILE = 'password.json'
PORT = 9090

class PasswordHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.password_file = PASSWORD_FILE
        self.load_password()
        super().__init__(*args, **kwargs)
    
    def load_password(self):
        self.data = {
            "password_hash": "07fceed9808e3263048adeb97c2cf41d5b817e5885fc8dd660958e0061393ea3",
            "password_me": "2b$12$ZMA.0Bnmtls9hIpstTOFwu41WcTA2tzevNgZcKSob6cPHVDT2M6ze"
        }
    
    def save_password(self):
        pass  # 密码固定，不保存到文件
    
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
        token = secrets.token_hex(16)
        self.data['access_token'] = token
        self.save_password()
        return token
    
    def verify_token(self, token):
        """验证访问令牌"""
        return self.data.get('access_token') == token
    
    def do_GET(self):
        print(f"接收到请求: {self.path}")
        if self.path == '/verify':
            # 处理密码验证
            password = self.headers.get('X-Password')
            print(f"收到密码验证请求，密码: {password}")
            data = self.load_password()
            
            if password and 'password_hash' in data:
                hashed = self.hash_password(password)
                print(f"密码哈希: {hashed}")
                print(f"存储的哈希: {data['password_hash']}")
                if hashed == data['password_hash']:
                    print("密码正确")
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
                    return
            
            print("密码错误")
            self.send_response(401)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'error', 'message': '密码错误'}).encode('utf-8'))
            return
        
        # 静态文件服务
        super().do_GET()

def main():
    try:
        print("密码文件已内置")
        
        # 启动服务器
        print(f"准备启动服务器在端口 {PORT}")
        with socketserver.TCPServer(("", PORT), PasswordHandler) as httpd:
            print(f"服务器启动在 http://localhost:{PORT}")
            print(f"请访问: http://localhost:{PORT}/index.html")
            httpd.serve_forever()
    except Exception as e:
        print(f"服务器启动失败: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()