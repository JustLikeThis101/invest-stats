# -*- coding: utf-8 -*-
"""
数据下载模块
支持 yfinance 和 akshare 两种数据源
"""

import yfinance as yf
import akshare as ak
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


def download_yfinance_data(tickers, start_date, period='max', interval='1d'):
    """
    下载 yfinance 数据
    
    Parameters:
    -----------
    tickers : list
        标的代码列表
    start_date : str
        开始日期，格式：'YYYY-MM-DD'
    period : str
        数据周期，默认 'max'
    interval : str
        数据间隔，默认 '1d'
    
    Returns:
    --------
    pandas.DataFrame or None
        下载的数据，失败时返回 None
    """
    print("📥 正在下载 yfinance 数据...")
    
    try:
        df = yf.download(
            tickers=tickers,
            period=period,
            interval=interval,
            auto_adjust=True,
            progress=False
        )
        
        # 按统一 start_date 裁剪
        df = df.loc[df.index >= pd.to_datetime(start_date)]
        
        print(f"✅ yfinance 数据下载完成，数据范围: {df.index[0].date()} → {df.index[-1].date()}")
        return df
        
    except Exception as e:
        print(f"❌ yfinance 数据下载失败: {e}")
        return None


def download_akshare_data(tickers_config, start_date):
    """
    下载 akshare 数据
    
    Parameters:
    -----------
    tickers_config : list
        标的配置列表，每个元素包含 'ticker' 和 'api_function'
    start_date : str
        开始日期，格式：'YYYY-MM-DD'
    
    Returns:
    --------
    pandas.DataFrame or None
        下载的数据，失败时返回 None
    """
    print("📥 正在下载 akshare 数据...")
    
    all_data = {}
    
    for config in tickers_config:
        ticker = config['ticker']
        api_function = config['api_function']
        
        try:
            # 获取对应的 akshare 函数
            func = getattr(ak, api_function)
            
            # 调用函数获取数据
            if api_function in ['stock_zh_index_daily', 'stock_zh_index_daily_tx']:
                df = func(symbol=ticker)
            else:
                df = func(symbol=ticker)
            
            # 确保日期列为 datetime 类型
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
                df.set_index('date', inplace=True)
            elif '日期' in df.columns:
                df['日期'] = pd.to_datetime(df['日期'])
                df.set_index('日期', inplace=True)
            
            # 按统一 start_date 裁剪
            df = df.loc[df.index >= pd.to_datetime(start_date)]
            
            # 重命名列为标准格式
            if 'close' in df.columns:
                df = df.rename(columns={'close': 'Close'})
            elif '收盘' in df.columns:
                df = df.rename(columns={'收盘': 'Close'})
            
            if not df.empty and 'Close' in df.columns:
                all_data[ticker] = df['Close'].dropna()
                print(f"✅ {ticker} 数据下载成功，数据点数: {len(df)}")
            else:
                print(f"⚠️ {ticker} 数据为空或缺少收盘价列")
                
        except Exception as e:
            print(f"❌ {ticker} 数据下载失败: {e}")
            continue
    
    if all_data:
        # 合并所有数据
        df_combined = pd.DataFrame(all_data)
        print(f"✅ akshare 数据下载完成，共 {len(all_data)} 个标的")
        return df_combined
    else:
        print("❌ akshare 数据下载失败，无有效数据")
        return None


def download_all_data(yfinance_tickers, akshare_tickers, start_date, period='max', interval='1d'):
    """
    下载所有数据源的完整数据
    
    Parameters:
    -----------
    yfinance_tickers : list
        yfinance 标的列表
    akshare_tickers : list
        akshare 标的配置列表
    start_date : str
        开始日期
    period : str
        数据周期
    interval : str
        数据间隔
    
    Returns:
    --------
    tuple
        (yf_data, ak_data) 两个数据源的DataFrame
    """
    print("🚀 开始下载所有数据源...")
    
    # 下载 yfinance 数据
    yf_data = download_yfinance_data(yfinance_tickers, start_date, period, interval)
    
    # 下载 akshare 数据
    ak_data = download_akshare_data(akshare_tickers, start_date)
    
    return yf_data, ak_data


# === 使用示例 ===
if __name__ == "__main__":
    # 示例：如何使用数据下载模块
    from tickers_config import yfinance_tickers, akshare_tickers
    
    # 下载数据
    yf_data, ak_data = download_all_data(
        yfinance_tickers=yfinance_tickers,
        akshare_tickers=akshare_tickers,
        start_date='2020-01-01'
    )
    
    print(f"yfinance 数据形状: {yf_data.shape if yf_data is not None else 'None'}")
    print(f"akshare 数据形状: {ak_data.shape if ak_data is not None else 'None'}")
