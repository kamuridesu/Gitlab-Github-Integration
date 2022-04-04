GITHUB_SSH=$1
GITLAB_SSH=$2

git clone $GITHUB_SSH temp
cd temp
git remote add gitlab $GITLAB_SSH
git branch -m main
git push -u gitlab main
cd ..
rm -rf temp
