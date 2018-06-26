# create collabs net
( cd ../CollabNet/ ; bash executeall.sh )

# serve
if [ "$1" == "-s" ]; then
  bundle exec jekyll build
  bundle exec jekyll serve
fi

if [ "$1" == "-p" ]; then
  git add .
  git commit -am "$2"
  git push
fi

