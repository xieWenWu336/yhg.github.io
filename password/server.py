#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地密码验证服务器
用于保护网站访问
"""

import http.server
import socketserver
import json
import hashlib
import os
import traceback

PORT = 9090
PASSWORD_FILE = 'password.json'

class PasswordHandler(http.server.SimpleHTTPRequestHandler):
    def load_password(self):
        try:
            if os.path.exists(PASSWORD_FILE):
                with open(PASSWORD_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"加载密码文件失败: {e}")
        return {}
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
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
        # 检查密码文件
        if not os.path.exists(PASSWORD_FILE):
            # 生成默认密码
            default_password = 'yhg123'
            hashed = hashlib.sha256(default_password.encode('utf-8')).hexdigest()
            
            with open(PASSWORD_FILE, 'w', encoding='utf-8') as f:
                json.dump({'password_hash': hashed}, f, ensure_ascii=False, indent=2)
            
            print(f"默认密码已设置: {default_password}")
            print("请运行 password_manager.py 来修改密码")
        else:
            print("密码文件已存在")
        
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