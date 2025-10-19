# -*- coding: utf-8 -*-
"""
Tickers 配置文件
包含 yfinance 和 akshare 数据源的标的配置
"""

# === yfinance 数据源配置 ===
# 支持美股、港股、日股、期货、加密货币等
# 格式: (ticker, 名称)
yfinance_tickers = [
    ('^GSPC', 'S&P 500'),
    ('^IXIC', '纳斯达克'),
    ('^NDX', '纳斯达克100'),
    ('^RUT', '罗素2000'),
    ('^SOX', '费城半导体指数'),
    ('^HSI', '恒生指数'),
    ('^N225', '日经指数'),
    ('159985.SZ', '豆粕ETF'),
    ('^NSEI', '印度NSE指数'),
    ('^GDAXI', '德国DAX指数'),
    ('601398.SS', '工商银行'),
    ('000001.SZ', '平安银行'),
    ('GC=F', '黄金期货'),
    ('SI=F', '白银期货'),
    ('HG=F', '铜期货'),
    ('AMZN', '亚马逊'),
    ('AAPL', '苹果'),
    ('MSFT', '微软'),
    ('GOOG', '谷歌'),
    ('META', '脸书'),
    ('TSLA', '特斯拉'),
    ('NVDA', '英伟达'),
    ('BTC-USD', '比特币'),
]

# === akshare 数据源配置 ===
# 使用字典列表，需要指定 ticker、名称和 api_function
# 如果没有安装 akshare，请注释掉这部分或设置为 []
akshare_tickers = [
    {
        'ticker': 'sh512890',
        'name': '红利低波',
        'api_function': 'stock_zh_index_daily_tx', 
    },
    {
        'ticker': 'sz399006',
        'name': '创业板',
        'api_function': 'stock_zh_index_daily',
    },
    {
        'ticker': 'sh000922',
        'name': '中证红利',
        'api_function': 'stock_zh_index_daily_tx',
    },
    {   
        'ticker': 'sh000001',
        'name': '上证指数',
        'api_function': 'stock_zh_index_daily',
    },
    {
        'ticker': 'sh000300',
        'name': '沪深300指数',
        'api_function': 'stock_zh_index_daily',
    }
]