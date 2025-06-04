import psycopg2
from psycopg2.extras import RealDictCursor
from rich.console import Console
import logging

console = Console()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode='w',
    filename='api.log',
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

try:
    host = 'localhost'
    user = 'username'
    password = 'dbpassword'
    db = 'dbname'
    
    connect = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db,
        cursor_factory=RealDictCursor
    )
    
    
    console.print('Database connected susccessfully!', style='green')
    logger.info('Database connected susccessfully!')
    
except Exception as e:
    console.print(f'Database connection failed ;-;\n{e}', style='red')
    logger.error(f'Database connection failed ;-;\n{e}')
       