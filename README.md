# AndroidEmuMacro

Automate Android tasks of emulator. It is made of a wrapper of adb in Python and object detection with OpenCV.  

*Also, this sourcecode is a prototype, so it may change a lot in the future.*  

# Quick start

Clone this project.

```
git clone https://github.com/Sachi854/android-emu-macro.git
```

This source not includes all necessary package.  
Because, you need to install these package as shown below.  

```
cd AndroidEmuMacro
pip install -r requirements.txt
```

Download [SDK Platform-Tools](https://developer.android.com/studio/releases/platform-tools) and pass through ``adb.exe`` path.

Enable adb of emulator from setting.  

Next, copy ``android_emu_macro.py`` and ``adb_wrapper.py``, ``object_detection.py`` to your project directory as shown below.  

```dir
your_project_dir
  ├── adb_wrapper.py
  ├── android_emu_macro.py
  ├── object_detection.py
  └── your_sourcecode.py
```

Import AndroidEmuMacro your sourcecode.

```py
import from android_emu_macro import AndroidEmuMacro
```

Create instance and code minimal statement.

```py
import from android_emu_macro import AndroidEmuMacro

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

Run this code.

# Usage

```
def __init__(self, adb_path="adb.exe", save_img_path="./imgs"):
    - Constructor.
        + adb_path : Path of adb.
        + save_img_pat : Path of save img.

def connect(self, device_address="localhost", device_port=5555) -> None:
    - Connect adb server of emulator.
        + device_address : IP address that can be checked in the settings of emulator.
        + device_port : Port that can be checked in the settings of emulator.
    
def disconnect(self) -> None:
    - Disconnect adb server of emulator.

def restart(self) -> None:
    - Restart adb server

def match_feature(self, train_img_path: str, threshold=4, sample_num=20, ratio=0.5, save_img=False) -> list:
    - Returns the coordinates of the image match.
    - Return object -> [is_match: Bool, [x: int, y: int]]
    - Algorithm is object detection.
    - Match for slightly obscure images.
        + train_img_path : Path of imput image. 
        + threshold : Minimum number of matches.
        + sample_num : Number of use mathe samlpe.
        + ratio : Parameter of ration test.
        + save_img : Save match img diff flag.

def match_template(self, train_img_path: str, threshold=0.8, save_img=False) -> list:
    - Returns the coordinates of the image match.
    - Return object -> [is_match: Bool, [x: int, y: int]]
    - Algorithm is template matching.
    - Match for per-pixel.
        + train_img_path : Path of imput image. 
        + threshold : Accuracy of match for per-pixel.
        + save_img : Save match img diff flag.

def match(self, train_img_path: str, save_img=False) -> list:
    - Returns the coordinates of the image match.
    - Return object -> [is_match: Bool, [x: int, y: int]]
    - Match for template or feature.
        + train_img_path : Path of imput image. 
        + save_img : Save match img diff flag.

def is_there_img(self, train_img_path: str, mode=0, save_img=False) -> bool:
    - Judge is there this image.
        + train_img_path : Path of imput image.
        + mode : 0 -> Template and feature, 1 -> Template only,2 -> Feature only
        + save_img : Save match img diff flag.

def tap_img(self, train_img_path: str, mode=0, save_img=False) -> bool:
    - Tap imput image.
        + train_img_path : Path of imput image.
        + mode : 0 -> Template and feature, 1 -> template only,2 -> feature only
        + save_img : Save match img diff flag.
        
def long_tap_img(self, train_img_path: str, m_sec=500, mode=0, save_img=False) -> bool:
    - Long tap imput image.
        + train_img_path : Path of imput image.
        + mode : 0 -> Template and feature, 1 -> template only,2 -> feature only
        + save_img : Save match img diff flag.

def swipe_img(self, train_img_path: str, x2: int, y2: int, m_sec=500, mode=0, save_img=False) -> bool:
    - Swipe imput image.
        + x2 : Terget coordinate of x.
        + y2 : Terget coordinate of y.
        + m_sec : Time of start btween end.
        + train_img_path : Path of imput image.
        + mode : 0 -> Template and feature, 1 -> Template only,2 -> Feature only
        + save_img : Save match img diff flag.    

def tap(self, x: int, y: int) -> None:
    - Tap imput coordinates.
        + x : Terget coordinate of x.
        + y : Terget coordinate of y.
        + save_img : Save match img diff flag.

def long_tap(self, x: int, y: int, m_sec=500) -> None:
    - Long tap imput coordinates.
        + x : Terget coordinate of x.
        + y : Terget coordinate of y.
        + save_img : Save match img diff flag.

def swipe(self, x1: int, y1: int, x2: int, y2: int, m_sec=500) -> None:
    - Swipe imput image.
        + x1 : Current coordinate of x.
        + y1 : Current coordinate of y.
        + x2 : Terget coordinate of x.
        + y2 : Terget coordinate of y.
        + m_sec : Time of start btween end.

def sleep(sec: float) -> None:
    - Sleep sec.
        + sec : sec.

def sleep_ms(m_sec: float) -> None:
    - Sleep micro sec.
        + m_sec : micro sec.


def screenshot(self, offset=1) -> None:
    - Take screen shot.
        + offset : Number of saveing
```

# Version

0.1 : Prototype released. -> (2020/12/31)

# おまけ

ドルフロ用マクロの使い方. 後で別のリポジトリに移すかも.  

*これ使って何らかの損害を被った場合, 一切責任を負いません(ライセンスにも明記されてます)*

## Download

リリースページからダウンロード

## 使い方

付属の``README.md``を読むこと