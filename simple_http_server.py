"""
简单的 HTTP 服务器，用于提供测试页面
"""

import http.server
import socketserver
import os
import threading
import time
from pathlib import Path


class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)
    
    def end_headers(self):
        # 添加 CORS 头，允许跨域请求
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # 处理根路径请求，返回测试页面
        if self.path == '/':
            self.path = '/test_page.html'
        # 处理其他路径请求，模拟路由
        elif self.path == '/login':
            self.path = '/test_page.html'
        elif self.path == '/home':
            self.path = '/test_page.html'
        elif self.path == '/profile':
            self.path = '/test_page.html'
        elif self.path == '/settings':
            self.path = '/test_page.html'
        
        return super().do_GET()
    
    def do_OPTIONS(self):
        # 处理预检请求
        self.send_response(200)
        self.end_headers()


def start_server(port=3000):
    """启动 HTTP 服务器"""
    handler = SimpleHTTPRequestHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"HTTP 服务器已启动，访问 http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n服务器已停止")


if __name__ == "__main__":
    start_server()