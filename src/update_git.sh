for d in ~/poc/scrapper/repos/*/; do
  echo "-------Updating $d--------"
  cd "$d"
  git pull
done