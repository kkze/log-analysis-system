from app import create_app

app = create_app()

# # 测试函数
# def test_app():
#     # 使用 Flask 测试客户端
#     with app.test_client() as client:
#         # 模拟登录以获取 token
#         response = client.post('/api/auth/login', json={    "username": "li","password": "042568"})
#         token = response.json['access_token']
        
#         # 使用获得的 token 访问受保护路由
#         response = client.post('/api/auth/logout', headers={'Authorization': f'Bearer {token}'})
#         print(response.json)


if __name__ == '__main__':
    app.run(debug=True)