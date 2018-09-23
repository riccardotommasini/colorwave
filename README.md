  524  docker network connect  tutorialrw greenstream
  525  docker network connect  tutorialrw bluestream
  526  docker run -d --rm -p 8181:8181 -p 8182-8200:8182-8200 --name jasper jasper
  527  docker network connect  tutorialrw jasper
  528  docker run -d -p 9292:9292 --rm --name streamhub streamhub
  529  docker rm -f streamhub
  530  docker run -d -p 9292:9292 --rm --name streamhub streamhub
  531  docker network connect  tutorialrw streamhub
  532  tail
  533  history
  534  history 10
  535* history 2
  536  history 12
  537  history 15
  538  history 16>history.md
  539  history 16 >> history.md
