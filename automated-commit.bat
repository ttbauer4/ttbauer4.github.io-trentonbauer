@echo off
title automated-commit.bat
cd C:\Users\trent\GitHub\ttbauer4.github.io-trentonbauer
git add .\pages\writing.html
git commit -m "added to writing page via automated commit"
git push
exit
