from app import app, db
from app.models import User

with app.app_context():
    db.create_all()
    
    # 创建管理员账户 (如果不存在)
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("管理员账户已创建: admin / admin123")

if __name__ == '__main__':
    app.run(debug=True)
