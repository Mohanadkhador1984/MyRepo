@echo off
chcp 65001 >nul
setlocal

:: ----------------------------------------
:: سكربت: sync_quizdb.bat
:: وصف: يصدر القاعدة محليًا ثم يستعيدها على Render
:: ----------------------------------------

:: 1) تعطيل SSL للاتصال المحلي
set "PGSSLMODE=disable"

:: 2) تصدير القاعدة المحلية بصيغة Custom
echo [1/2] Dumping local database quizdb1...
pg_dump -U postgres -d quizdb1 -Fc -v -f local_quizdb.dump
if errorlevel 1 (
  echo ERROR: Failed to dump local DB
  pause
  exit /b 1
)

:: 3) تفعيل SSL للاتصال البعيد
set "PGSSLMODE=require"
set "PGPASSWORD=uYMGKY953sG7jQhfJGsAYS3yDpmOJwS7"

:: 4) استعادة dump على خادم Render
echo [2/2] Restoring to Render database quizdb1_li31...
pg_restore ^
  -h dpg-d1voaker433s73fsuk00-a.oregon-postgres.render.com ^
  -p 5432 ^
  -U quizdb1_li31_user ^
  -d quizdb1_li31 ^
  --clean ^
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
echo 🎉 Database sync completed successfully!
pause
endlocal
