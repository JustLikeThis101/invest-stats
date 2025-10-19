import ffn
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# 导入配置和下载模块
from tickers_config import yfinance_tickers, akshare_tickers
from data_downloader import download_yfinance_data, download_akshare_data

# === 通用参数 ===
period = 'max'
interval = '1d'
start_date = '1992-01-02'  # 统一起始日期


def analyze_ticker_performance(series, ticker_name):
    """分析单个标的的性能指标"""
    print(f"\n==================== {ticker_name} ====================")
    
    if series.empty:
        print(f"⚠️ {ticker_name} 数据为空，跳过。")
        return
    
    series.name = ticker_name
    print(f"数据范围: {series.index[0].date()} → {series.index[-1].date()}")
    print(f"数据点数: {len(series)}")
    print("价格预览：")
    print(series.head())

    # 计算性能指标
    try:
        stats = ffn.PerformanceStats(series)
        
        # 打印指标表
        print("\n绩效指标：")
        stats.display()

        # 绘图
        stats.plot()
        plt.title(f"{ticker_name} Performance (ffn)")
        plt.show()
        
    except Exception as e:
        print(f"❌ {ticker_name} 性能分析失败: {e}")

# === 主程序 ===
def main():
    print("🚀 开始多数据源市场分析...")
    print(f"📅 统一开始时间: {start_date}")
    
    # 下载 yfinance 数据
    yf_data = download_yfinance_data(yfinance_tickers, start_date, period, interval)
    
    # 下载 akshare 数据
    ak_data = download_akshare_data(akshare_tickers, start_date)
    
    # 分析 yfinance 数据
    if yf_data is not None:
        print(f"\n📊 开始分析 yfinance 数据 ({len(yfinance_tickers)} 个标的)...")
        
        for ticker in yfinance_tickers:
            try:
                # 处理 MultiIndex 列
                if isinstance(yf_data.columns, pd.MultiIndex):
                    series = yf_data[('Close', ticker)].dropna()
                else:
                    series = yf_data[ticker].dropna()
                
                analyze_ticker_performance(series, ticker)
                
            except KeyError:
                print(f"⚠️ 无法找到 {ticker} 的数据，跳过。")
                continue
            except Exception as e:
                print(f"❌ {ticker} 分析失败: {e}")
                continue
    
    # 分析 akshare 数据
    if ak_data is not None:
        print(f"\n📊 开始分析 akshare 数据 ({len(ak_data.columns)} 个标的)...")
        
        for ticker in ak_data.columns:
            try:
                series = ak_data[ticker].dropna()
                analyze_ticker_performance(series, ticker)
                
            except Exception as e:
                print(f"❌ {ticker} 分析失败: {e}")
                continue
    
    print("\n🎉 所有分析完成！")

if __name__ == "__main__":
    main()
