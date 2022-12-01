from app import app
from app.app_account import account_bp
from app.app_demo import demo_bp
from app.app_map import map_bp
from app.app_carbon import carbon_bp

app.register_blueprint(account_bp)
app.register_blueprint(demo_bp)
app.register_blueprint(map_bp)
app.register_blueprint(carbon_bp)

if __name__ == '__main__':
    print('Test Addr: 127.0.0.1:5000')
    app.run(
        host='127.0.0.1',
        port='5000',
        debug=True
        )
