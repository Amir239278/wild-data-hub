@echo off
setlocal enabledelayedexpansion

REM 🚀 Lancer le container dvf_job avec vérification du volume monté

set "PROJET_PATH=%~dp0"

REM 🧼 Supprimer le container si existant
docker rm -f dvf_job >nul 2>&1

REM 🐳 Lancer le container avec montage du dossier local
docker run -d --name dvf_job ^
  -v "%PROJET_PATH%dataset:/app/dataset" ^
  dvf-collector

echo.
echo ---------------------------------------
echo 🎉 Container dvf_job lancé avec succès
echo 📂 Volume monté : %PROJET_PATH%dataset
echo ---------------------------------------

REM ⏱️ Pause pour laisser cron démarrer
timeout /t 5 >nul

REM 📊 Vérification du fichier de log
echo.
echo 🔍 Vérification du fichier de log dvf.log...
docker exec dvf_job sh -c "if [ -f /app/dataset/dvf.log ]; then echo ✅ dvf.log trouvé ; stat -c '🕒 Dernière modification : %%y' /app/dataset/dvf.log ; echo 🔽 Contenu récent : ; tail -n 5 /app/dataset/dvf.log ; else echo ❌ dvf.log non trouvé ; fi"

REM 📂 Liste des fichiers DVF générés (.csv.gz)
echo.
echo 📁 Fichiers DVF présents dans /app/dataset :
docker exec dvf_job sh -c "ls -lh /app/dataset/*.csv.gz 2>/dev/null || echo Aucun fichier .csv.gz trouvé"

echo.
echo ✅ Fin du script — vérifie dvf.log pour confirmer l'exécution
pause
endlocal

