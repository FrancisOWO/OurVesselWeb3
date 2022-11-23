from app import app
from app.wtc_account import account_bp
from app.wtc_demo import demo_bp

app.register_blueprint(account_bp)
app.register_blueprint(demo_bp)

if __name__ == '__main__':
    print('Test Addr: 127.0.0.1:5000')
    app.run(
        host='127.0.0.1',
        port='5000',
        debug=True
        )
