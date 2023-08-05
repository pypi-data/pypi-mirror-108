@echo off
echo add
echo update
echo fixbug
echo relase
echo version
echo --------------------------------------
set /p msg=nhap noi dung chinh sua: 
git add .
git commit -m "%msg%"
git push -u origin master
echo.
echo --------------------------------------
echo Commit thanh cong, xem log cac version
echo Version hien tai: %msg%
echo --------------------------------------
echo.
cls
git log --pretty=oneline -10
pause