@echo off
chcp 65001 >nul

echo 请选择执行的目标操作：
echo   I^) 安装并运行 
echo   R^) 仅运行 
set /p option="> "

if /i "%option%"=="I" goto install_and_run
if /i "%option%"=="R" goto run

echo 非法输入.
exit /b 1

:install_and_run
echo 正在创建虚拟环境...
python -m venv venv
call venv\Scripts\activate
echo 正在安装必要库...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
call deactivate

:run
echo 正在激活虚拟环境...
python -m venv venv
call venv\Scripts\activate
echo 虚拟环境激活完毕
python main.py

:end
pause
