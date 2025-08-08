# INSTRUCCIONES PARA EJECUTAR EL SERVIDOR BACKEND

## M+�todo 1: Usando PowerShell
1. Abre PowerShell como administrador
2. Navega al directorio del backend:
   ```
   cd "c:\Users\36705\Desktop\Nueva carpeta (4)\KandaProyect\KandaBackEnd"
   ```
3. Activa el entorno virtual:
   ```
   .\venv\Scripts\Activate.ps1
   ```
4. Ejecuta el servidor:
   ```
   python manage.py runserver
   ```

## M+�todo 2: Usando el script PowerShell creado
1. Abre PowerShell como administrador
2. Ejecuta:
   ```
   .\run_server.ps1
   ```

## M+�todo 3: Usando el archivo batch
1. Haz doble clic en `run_server.bat`

## Verificar que funciona
- El servidor deber+�a iniciar en http://127.0.0.1:8000/
- Verifica que puedas acceder a http://127.0.0.1:8000/api/characters/

## Soluci+�n de problemas
Si tienes errores de permisos en PowerShell, ejecuta:
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

## Cambios realizados en el c+�digo:
1. ԣ� Serializer actualizado con campos age, special_abilities, goals
2. ԣ� Frontend modificado para enviar datos en formato correcto
3. ԣ� Mejorado manejo de errores para mejor debugging
4. ԣ� Payload mapeado correctamente:
   - personality ��� personality_traits (array)
   - physical_description ��� physical_traits (array)  
   - history ��� background
   - weaknesses convertido a array
