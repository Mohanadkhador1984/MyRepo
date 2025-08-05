@echo off
chcp 65001 >nul
setlocal

:: ----------------------------------------
:: سكربت: reset_sync_quizdb.bat
:: وصف: يحذف كامل البيانات من خادم Render ثم يستورد dump جديد
:: ----------------------------------------

:: 1) تعطيل SSL للاتصال المحلي
set "PGSSLMODE=disable"

:: 2) تصدير القاعدة المحلية بصيغة Custom
echo [1/3] Dumping local database quizdb1...
pg_dump -U postgres -d quizdb1 -Fc -v -f local_quizdb.dump
if errorlevel 1 (
  echo ERROR: Failed to dump local DB
  pause
  exit /b 1
)

:: 3) تفعيل SSL للاتصال البعيد وتعيين كلمة المرور
set "PGSSLMODE=require"
set "PGPASSWORD=uYMGKY953sG7jQhfJGsAYS3yDpmOJwS7"

:: 4) حذف كامل البيانات على Render (drop + recreate public schema)
echo [2/3] Dropping all objects on Render...
psql ^
  -h dpg-d1voaker433s73fsuk00-a.oregon-postgres.render.com ^
  -p 5432 ^
  -U quizdb1_li31_user ^
  -d quizdb1_li31 ^
  -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;" 
if errorlevel 1 (
  echo ERROR: Failed to clean remote DB
  pause
  exit /b 1
)

:: 5) استعادة dump على خادم Render
echo [3/3] Restoring dump to Render database...
pg_restore ^
  -h dpg-d1voaker433s73fsuk00-a.oregon-postgres.render.com ^
  -p 5432 ^
  -U quizdb1_li31_user ^
  -d quizdb1_li31 ^
  --no-owner ^
  --role=quizdb1_li31_user ^
  --jobs=4 ^
  --verbose ^
  local_quizdb.dump
if errorlevel 1 (
  echo ERROR: Failed to restore on Render
  pause
  exit /b 1
)

echo.
echo 🎉 Reset and sync completed successfully!
pause
endlocal
