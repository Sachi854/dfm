# DFM 

どOふろ制御用ライブラリ

# Quick start

クローンとサブモジュールの同期

```
git clone https://github.com/Sachi854/dfm.git
cd dfm
git submodule update --init --recursive
```

仮想環境を作る&有効化

```bash
python3 -m venv venv
source venv/bin/activate
```

AEMをインストール

```bash
cd AndroidEmuMacro
python ./setup.py install
pip install -r requirements.txt
```

適当にdfm以下をimport

```python
import dfm.base as bs
```

あとは頑張れ

# Usages

あとで書く

# License  

[MIT LICENSE](https://github.com/Sachi854/dnf/blob/master/LICENSE) 
