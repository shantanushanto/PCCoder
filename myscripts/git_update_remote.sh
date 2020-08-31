#!/bin/bash

# Don't up this file to github

usr=$git_usr
pss=$git_pss

prjdir="RPS"
# ------------- Pushing to github (needed if http is used in github) -----------------
#function git_github(){
#  github=$(git remote get-url --push origin)
#  prefix=${github:0:8}
#  suffix=${github:8}
#  url_github="${prefix}${usr}:${pss}@${suffix}"
#}

#git_github

echo "-> pushing to github.. Started"
# git push $url_github master # (needed if http is used in github)
git push origin master
echo "pushing to github.. Completed."

# ------------- Pulling in Palab -----------------
echo "-> pulling to palab.. Started"
# ssh -q shanto@palab.cse.tamu.edu "cd work/RPS && git pull $url_github master" # (needed if http is used in github)
ssh -q shanto@palab.cse.tamu.edu "cd work/$prjdir && git pull origin master && git submodule update"
echo "pulling to palab.. Completed."

# ------------- Pulling in Atlas -----------------
echo "-> pulling to atlas.. Started"
#ssh -q atlas@engr.tamu.edu "cd work/RPS && git pull $url_github master" # (needed if http is used in github)
sshpass -p $tamu_pss ssh -q shanto@atlas.engr.tamu.edu "cd work/$prjdir && git pull origin master && git submodule update"
echo "pulling to atlas.. Completed."