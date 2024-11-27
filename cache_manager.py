import functools
import time
from datetime import datetime
import pickle
import os

def cache_data(expire_time=3600):
    """データキャッシュデコレータ"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # キャッシュキーの生成
            cache_key = f"{func.__name__}_{str(args)}_{str(kwargs)}"
            cache_file = f".cache/{cache_key}.pkl"
            
            # キャッシュディレクトリの作成
            os.makedirs(".cache", exist_ok=True)
            
            # キャッシュの確認
            if os.path.exists(cache_file):
                try:
                    with open(cache_file, 'rb') as f:
                        cached_data = pickle.load(f)
                    
                    # キャッシュの有効期限チェック
                    if time.time() - cached_data['timestamp'] < expire_time:
                        return cached_data['data']
                except (EOFError, pickle.PickleError, KeyError) as e:
                    # キャッシュファイルが破損している場合は削除
                    os.remove(cache_file)
                    print(f"破損したキャッシュファイルを削除しました: {cache_file}")
            
            # 新しいデータの取得
            data = func(*args, **kwargs)
            
            # キャッシュの保存
            with open(cache_file, 'wb') as f:
                pickle.dump({
                    'data': data,
                    'timestamp': time.time()
                }, f)
            
            return data
        return wrapper
    return decorator

def clear_expired_cache(expire_time=3600):
    """期限切れキャッシュの削除"""
    if not os.path.exists(".cache"):
        return
        
    current_time = time.time()
    for cache_file in os.listdir(".cache"):
        file_path = os.path.join(".cache", cache_file)
        if current_time - os.path.getmtime(file_path) > expire_time:
            os.remove(file_path)
