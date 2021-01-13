# AndroidEmuMacro

Automate Android tasks of emulator. It is made of a wrapper of adb in Python and object detection with OpenCV.  

*Also, this sourcecode is a prototype, so it may change a lot in the future.*  

# Quick start

Clone this project.

```
https://github.com/Sachi854/AndroidEmuMacro.git
```

This source not includes all necessary package.  
Because, you need to install these package as shown below.  

```
cd AndroidEmuMacro
pip install -r requirements.txt
```

Download [SDK Platform-Tools](https://developer.android.com/studio/releases/platform-tools) and pass through ``adb.exe`` path.

Enable adb of emulator from setting.  

Next, copy ``aem`` to your project directory as shown below.  

```dir
your_project_dir
  ├── aem 
  └── your_sourcecode.py
```

Try, as shown below.  

```python
import aem

if __name__ == '__main__':
    # create instance
    aem = aem.AndroidEmuMacro()
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

```python
def __init__(self, adb_path="adb.exe", save_img_path="./imgs"):
    """
    Constructor.

    Parameters:
    ----------
    adb_path : str 
        Path of adb.
    save_img_path : str
        Path of save img.
    """
    pass


def connect(self, device_address="localhost", device_port=5555) -> None:
    """
    Connect adb server of emulator.
    
    Parameters:
    ----------
    device_address : str
        IP address that can be checked in the settings of emulator.
    device_port : str
        Port that can be checked in the settings of emulator.
    """
    pass
    

def disconnect(self) -> None:
    """
    Disconnect adb server of emulator.
    """
    pass


def restart(self) -> None:
    """
    Restart adb server
    """
    pass


def match_feature(self, train_img_path: str, threshold=4, sample_num=20, ratio=0.5, save_img=False) -> list:
    """
    Returns the coordinates of the image match.
    Algorithm is object detection.
    Match for slightly obscure images.
    
    Parameters:
    ----------
    train_img_path : str
        Path of input image. 
    threshold : int
        Minimum number of matches.
    sample_num : int
        Number of use mathe sample.
    ratio : float
        Parameter of ration test.
    save_img : bool
        Save match img diff flag.
    
    Returns:
    ----------
    list
        [is_match: Bool, [x: int, y: int]]
    """
    pass


def match_template(self, train_img_path: str, threshold=0.8, save_img=False) -> list:
    """
    Returns the coordinates of the image match.
    Algorithm is template matching.
    Match for per-pixel.
    
    Parameters:
    ----------
    train_img_path : str
        Path of input image. 
    threshold : float
        Accuracy of match for per-pixel.
    save_img : bool
        Save match img diff flag.
    
    Returns:
    ----------
    list
        [is_match: Bool, [x: int, y: int]]
    """
    pass


def match(self, train_img_path: str, save_img=False) -> list:
    """
    Returns the coordinates of the image match.
    Match for template or feature.
    
    Parameters:
    ----------
    train_img_path : str
        Path of input image. 
    save_img : bool
        Save match img diff flag.
    
    Returns:
    ----------
    list
        [is_match: Bool, [x: int, y: int]]
    """
    pass


def is_there_img(self, train_img_path: str, mode=0, save_img=False) -> bool:
    """
    Judge is there this image.
    
    Parameters:
    ----------
    train_img_path : str
        Path of input image.
    mode : int
        0 -> Template and feature, 1 -> Template only,2 -> Feature only
    save_img : bool
        Save match img diff flag.
    
    Returns:
    ----------
    bool
    """
    pass


def tap_img(self, train_img_path: str, mode=0, save_img=False) -> bool:
    """
    Tap input image.
    
    Parameters:
    ----------
    train_img_path : str 
        Path of input image.
    mode : int
        0 -> Template and feature, 1 -> template only,2 -> feature only
    save_img : bool
        Save match img diff flag.
    
    Returns:
    ----------
    bool
    """
    pass

 
def long_tap_img(self, train_img_path: str, m_sec=500, mode=0, save_img=False) -> bool:
    """
    Long tap input image.
    
    Parameters:
    ----------
    train_img_path : str
        Path of input image.
    mode : int
        0 -> Template and feature, 1 -> template only,2 -> feature only
    save_img : bool
        Save match img diff flag.
    
    Returns:
    ----------
    bool
    """
    pass


def swipe_img(self, train_img_path: str, x2: int, y2: int, m_sec=500, mode=0, save_img=False) -> bool:
    """
    Swipe input image.
    
    Parameters:
    ----------
    train_img_path : int
        Path of input image.
    x2 : int
        target coordinate of x.
    y2 : int
        target coordinate of y.
    m_sec : int
        Time of start between end.
    mode : int
        0 -> Template and feature, 1 -> Template only,2 -> Feature only
    save_img : bool
        Save match img diff flag.    

    Returns:
    ----------
    bool
    """
    pass


def tap(self, x: int, y: int) -> None:
    """
    Tap input coordinates.
    
    Parameters:
    ----------
    x : int
        target coordinate of x.
    y : int
        target coordinate of y.
    save_img : str
        Save match img diff flag.
    """
    pass


def long_tap(self, x: int, y: int, m_sec=500) -> None:
    """
    Long tap input coordinates.
    
    Parameters:
    ----------
    x : int
        target coordinate of x.
    y : int
        target coordinate of y.
    save_img : str
        Save match img diff flag.
    """
    pass


def swipe(self, x1: int, y1: int, x2: int, y2: int, m_sec=500) -> None:
    """
    Swipe input coordinates to target coordinates.
    
    Parameters:
    ----------
    x1 : int
        Current coordinate of x.
    y1 : int
        Current coordinate of y.
    x2 : int
        target coordinate of x.
    y2 : int
        target coordinate of y.
    m_sec : int 
        Time of start between end.
    """
    pass

def sleep(sec: float) -> None:
    """
    Sleep sec.
    
    Parameters:
    ----------
    sec : float
        sec.
    """
    pass    


def sleep_ms(m_sec: float) -> None:
    """
    Sleep micro sec.
    
    Parameters:
    ----------
    m_sec : float
        micro sec.
    """
    pass


def screenshot(self, offset=1) -> None:
    """
    Take screen shot.
    
    Parameters:
    ----------
    offset : int
        Number of saving
    """
    pass
```

# Version

0.1 : Prototype released. -> (2020/12/31)

# License

MIT License  
