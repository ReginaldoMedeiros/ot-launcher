@echo off
REM Uso: tools\publicar-client.cmd <versao> <pasta_do_client>
REM Ex.: tools\publicar-client.cmd 1.0.0 D:\Otserver\_dist\CrystalClient
python "%~dp0publicar-client.py" %1 %2
