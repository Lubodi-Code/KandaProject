@echo off
cd "c:\Users\36705\Desktop\Nueva carpeta (4)\KandaProyect\KandaBackEnd"
echo Activando entorno virtual...
call venv\Scripts\activate.bat
echo Iniciando servidor Django...
python manage.py runserver
pause
