@echo off
title commit.bat
cd C:\Users\trent\GitHub\ttbauer4.github.io-trentonbauer
git add .\pages\writing.html
git add .\images\%1
git commit -m "added to writing page via automated commit"
git push
exit
