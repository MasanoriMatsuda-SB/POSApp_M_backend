# database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# .env ファイルを読み込む
load_dotenv()

# 環境変数から取得
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "pos_app_matsuda")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "password")

# SSL証明書のパスを設定（相対パス）
CERT_PATH = os.path.join(os.path.dirname(__file__), "certificates", "DigiCertGlobalRootCA.crt.pem")

# DB接続URLを組み立て (pymysqlを使用)
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    f"?ssl_ca={CERT_PATH}&ssl_verify_cert=true"
)

try:
    # Engine と SessionLocal を生成（SSL設定付き）
    engine = create_engine(
        DATABASE_URL,
        echo=True,  # SQLログを出力
        connect_args={
            "ssl": {
                "ssl_ca": CERT_PATH
            }
        }
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    print(f"データベース接続エラー: {e}")
