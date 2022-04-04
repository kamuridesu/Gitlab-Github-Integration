GITLAB_SSH=$1
GITHUB_SSH=$2

git clone $GITLAB_SSH temp
cd temp
git remote add github $GITHUB_SSH
git branch -m main
git push -u github main
cd ..
rm -rf temp
