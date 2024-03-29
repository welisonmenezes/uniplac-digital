from datetime import timedelta

# Configurações de ambiente
ENV = 'development'
DEBUG = True
TEMPLATES_AUTO_RELOAD = True

# Configurações de banco de dados
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/uniplacdigital'

#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://welison:menezes85@welison.mysql.pythonanywhere-services.com/welison$uniplacdigital'

# Configurações de segurança
SECRET_KEY = '#$#gdFDKF#993FDVKkfdkj#$$2@@@@dfdlafFGÇPLO^dfe__fd'
PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
USE_PERMANENT_SESSION = True

# Configurações de email
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'uniplacdigital@gmail.com'
MAIL_PASSWORD = 'ud1902@wlg'