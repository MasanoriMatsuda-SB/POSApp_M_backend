# database.py
import os
import urllib.parse
import logging
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ロギング設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# .env ファイルを読み込む
load_dotenv()

# 環境変数から取得
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "pos_app_matsuda")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "password")

# パスワードをURLエンコード
encoded_password = urllib.parse.quote_plus(DB_PASS)

# SSL証明書のパスを設定（相対パス）
CERT_PATH = os.path.join(os.path.dirname(__file__), "certificates", "DigiCertGlobalRootG2.crt.pem")

# 接続情報のログ出力
logger.info(f"DB接続情報:")
logger.info(f"HOST: {DB_HOST}")
logger.info(f"PORT: {DB_PORT}")
logger.info(f"NAME: {DB_NAME}")
logger.info(f"USER: {DB_USER}")

# DB接続URLを組み立て (pymysqlを使用)
DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
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
    
    # 接続テスト
    with engine.connect() as connection:
        result = connection.execute("SELECT 1")
        logger.info(f"接続テスト結果: {result.scalar()}")
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logger.error(f"データベース接続エラー: {type(e)}")
    logger.error(f"エラー詳細: {e}")
