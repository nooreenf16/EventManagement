from website import create_app

import pymysql
pymysql.version_info = (1, 4, 6, 'final', 0)
pymysql.install_as_MySQLdb()

app = create_app()

if __name__ == '__main__':
    
    app.run(debug=True)

