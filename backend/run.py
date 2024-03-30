from app import create_app

app = create_app()


# 打印所有路由

# with app.app_context():  # 确保应用上下文激活
#     print('Available routes:')
#     for rule in app.url_map.iter_rules():
#         print(rule.endpoint, rule.rule, list(rule.methods))
if __name__ == '__main__':
    app.run()