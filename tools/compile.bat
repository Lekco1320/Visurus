@echo off

nuitka ^
--standalone ^
--mingw64 ^
--onefile ^
--enable-plugin=tk-inter ^
--nofollow-import-to=requests,numpy ^
--remove-output ^
--output-dir=. ^
--output-filename="Visurus" ^
--windows-company-name=Lekco ^
--windows-product-name="Lekco Visurus" ^
--windows-product-version=1.0.1.196 ^
--windows-icon-from-ico=.\logo.ico ^
..\src\main.py

move .\Visurus.exe ..\src
