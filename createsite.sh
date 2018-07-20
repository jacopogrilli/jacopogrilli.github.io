# create collabs net
( cd ../CollabNet/ ; bash executeall.sh )

# serve
cp ../../Cv/aggiornato/jgrilli_cv.pdf ./images/

if [ "$1" == "-s" ]; then

  for p in `ps aux | grep jekyll | awk '{print $2}'`; do
      kill $p
  done

  bundle exec jekyll build
  xterm -hold -e bundle exec jekyll serve &
  sleep 3s
  google-chrome http://127.0.0.1:4000/ &
fi




if [ "$1" == "-p" ]; then
  git add .
  git commit -am "$2"
  git push
fi

