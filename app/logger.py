import logging

from app.config import LOG_DIR

#log出力先ファイルを作成
LOG_FILE = LOG_DIR / "monthly-report.log"

#出力するファイル、記録するlogのレベル指定、記録する内容
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)
