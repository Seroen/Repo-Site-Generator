:: Compile website
python3 repo_core.py
echo Website compiled

:: Commit website
cd ./website

git add -A
git commit -m "Quick website commit"
git push -u origin main

cd ..

del input/Website/.git
xcopy /s Website/.git input/Website/.git

echo Website commited

:: Commit repo
cd ./input/Modded-Regions-Starter-Pack-main

git add -A
git commit -m "Quick repo commit"
git push -u origin main

cd ../..

:: Commit website source
git add -A
git commit -m "Quick source commit"
git push -u origin main

pause
