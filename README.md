# AndroidEmuMacro

Android Emulatorの操作を自動化するライブラリ. ADBのラッパーとOpenCVを用いた物体検出で実装してある.

*これだたのプロタイプだから仕様はめちゃくちゃに変更されると予想されるよ!*  

# Quick start

このプロジェクトをクローン.  

```
https://github.com/Sachi854/AndroidEmuMacro.git
```

以下のコマンドでパッケージの依存関係にあるパッケージをインストール.  

```
cd AndroidEmuMacro
pip install -r requirements.txt
```

[SDK Platform-Tools](https://developer.android.com/studio/releases/platform-tools) をダウンロードして ``adb.exe`` のパスを通す.  

エミュレータの設定からADBを有効にする.    

次に``android_emu_macro.py`` と ``adb_wrapper.py``, ``object_detection.py`` を自分のプロジェクトのフォルダに以下の配置になるようコピー.  

```dir
your_project_dir
  ├── adb_wrapper.py
  ├── android_emu_macro.py
  ├── object_detection.py
  └── your_sourcecode.py
```

以下のようにコードを書いてみる.  

```python
from android_emu_macro import AndroidEmuMacro

if __name__ == '__main__':
    # create inctance
    aem = AndroidEmuMacro()
    # connect emulator
    aem.connect()
    aem.sleep(2)

    # tap display
    aem.tap(200,400)    

    # disconnect emulator
    aem.disconnect()
```

実行してみる.  

# Usage

```pydocstring
def __init__(self, adb_path="adb.exe", save_img_path="./imgs"):
    """
    コンストラクタ

    Parameters
    ----------
    adb_path : str 
        adbのパス
    save_img_pat : str
        一時的に画像を保管したりするディレクトリのパス
    """
    pass


def connect(self, device_address="localhost", device_port=5555) -> None:
    """
    ADBサーバに接続
    
    Parameters
    ----------
    device_address : str
        エミュレータの設定から確認できる ADBサーバのip address
    device_port : str
        エミュレータの設定から確認できる ADBサーバのポート番号
    """
    pass
    

def disconnect(self) -> None:
    """
    ADBサーバから切断
    """
    pass


def restart(self) -> None:
    """
    ADBサーバを再起動
    """
    pass


def match_feature(self, train_img_path: str, threshold=4, sample_num=20, ratio=0.5, save_img=False) -> list:
    """
    画面と画像をマッチングしその座標を返す
    アルゴリズムは特徴量検出
    曖昧な画像検出向け
    
    Parameters
    ----------
    train_img_path : str
        入力画像のパス 
    threshold : int
        マッチ数の下限
    sample_num : int
        使用するサンプル数
    ratio : float
        ratioテストに使用するパラメータ
    save_img : bool
        マッチした画像を保存するかどうか
    
    Returns:
    ----------
    list
        [is_match: Bool, [x: int, y: int]]
    """
    pass


def match_template(self, train_img_path: str, threshold=0.8, save_img=False) -> list:
    """
    画面と画像をマッチングしその座標を返す
    アルゴリズムはテンプレートマッチング
    ピクセル単位での正確なマッチング
    
    Parameters
    ----------
    train_img_path : str
        入力画像のパス 
    threshold : float
        マッチングの精度(0~1.0)
    save_img : bool
        マッチした画像を保存するかどうか
    
    Returns:
    ----------
    list
        [is_match: Bool, [x: int, y: int]]
    """
    pass


def match(self, train_img_path: str, save_img=False) -> list:
    """
    画面と画像をマッチングしその座標を返す
    テンプレートを優先でダメらな特徴量でマッチングさせる
    
    Parameters
    ----------
    train_img_path : str
        入力画像のパス  
    save_img : bool
        マッチした画像を保存するかどうか
    
    Returns:
    ----------
    list
        [is_match: Bool, [x: int, y: int]]
    """
    pass


def is_there_img(self, train_img_path: str, mode=0, save_img=False) -> bool:
    """
    画面にその画像があるか判定
    
    Parameters
    ----------
    train_img_path : str
        入力画像のパス  
    mode : int
        0 -> テンプレートマッチングと特徴量のどっちも, 1 -> テンプレートのみ,2 -> 特徴量のみ
    save_img : bool
        マッチした画像を保存するかどうか
    
    Returns:
    ----------
    bool
    """
    pass


def tap_img(self, train_img_path: str, mode=0, save_img=False) -> bool:
    """
    画面内にその画像があればタップ
    
    Parameters
    ----------
    train_img_path : str 
        入力画像のパス  
    mode : int
        0 -> テンプレートマッチングと特徴量のどっちも, 1 -> テンプレートのみ,2 -> 特徴量のみ
    save_img : bool
        マッチした画像を保存するかどうか
    
    Returns:
    ----------
    bool
    """
    pass

 
def long_tap_img(self, train_img_path: str, m_sec=500, mode=0, save_img=False) -> bool:
    """
    画面内にその画像があればロングタップ
    
    Parameters
    ----------
    train_img_path : str 
        入力画像のパス  
    mode : int
        0 -> テンプレートマッチングと特徴量のどっちも, 1 -> テンプレートのみ,2 -> 特徴量のみ
    save_img : bool
        マッチした画像を保存するかどうか
    
    Returns:
    ----------
    bool
    """
    pass


def swipe_img(self, train_img_path: str, x2: int, y2: int, m_sec=500, mode=0, save_img=False) -> bool:
    """
    画面内にその画像があれば指定位置までスワイプ
    
    Parameters
    ----------
    train_img_path : int
        入力画像のパス  
    x2 : int
        x軸ターゲット座標
    y2 : int
        y軸ターゲット座標
    m_sec : int
        スワイプにかかる時間をミリ秒で指定
    mode : int
        0 -> テンプレートマッチングと特徴量のどっちも, 1 -> テンプレートのみ,2 -> 特徴量のみ
    save_img : bool
        マッチした画像を保存するかどうか

    Returns:
    ----------
    bool
    """
    pass


def tap(self, x: int, y: int) -> None:
    """
    入力位置をタップ
    
    Parameters
    ----------
    x : int
        x軸ターゲット座標
    y : int
        y軸ターゲット座標
    save_img : str
        マッチした画像を保存するかどうか
    """
    pass


def long_tap(self, x: int, y: int, m_sec=500) -> None:
    """
    入力位置をロングタップ
    
    Parameters
    ----------
    x : int
        x軸ターゲット座標
    y : int
        y軸ターゲット座標
    save_img : str
        マッチした画像を保存するかどうか
    """
    pass


def swipe(self, x1: int, y1: int, x2: int, y2: int, m_sec=500) -> None:
    """
    入力位置をターゲット位置までスワイプ
    
    Parameters
    ----------
    x1 : int
        x軸入力座標
    y1 : int
        y軸入力座標
    x2 : int
        x軸ターゲット座標
    y2 : int
        y軸ターゲット座標
    m_sec : int
        スワイプにかかる時間をミリ秒で指定
    """
    pass

def sleep(sec: float) -> None:
    """
    スリープ
    
    Parameters
    ----------
    sec : float
        秒
    """
    pass    


def sleep_ms(m_sec: float) -> None:
    """
    スリープ
    
    Parameters
    ----------
    m_sec : float
        ミリ秒
    """
    pass


def screenshot(self, offset=1) -> None:
    """
    スクリーンショットを撮る
    
    Parameters
    ----------
    offset : int
        セーブ画像の背中につく番号
    """
    pass
```

# Version

0.1 : プロトタイプのリリース. -> (2020/12/31)

# License

MIT License  

# おまけ

ドルフロ用マクロの使い方. 後で別のリポジトリに移すかも.  

*これ使って何らかの損害を被った場合, 一切責任を負いません(ライセンスにも明記されてます)*

## Download

リリースページからダウンロード

## 使い方

付属の``README.md``を読むこと
