@echo off
chcp 65001 >nul

for /r "..\src" %%d in (.) do (
    if "%%~nxd"=="__pycache__" (
        echo 正在删除：%%d
        rmdir /s /q "%%d"
    )
)

echo 编译缓存清理完毕.
