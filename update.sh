#!/bin/sh

# 업데이트 스크립트 진행하여 코드 최신화
# git pull -> docker rebuild -> main.py run

sudo docker rm -f $(docker ps -qa)

# 빌드할 때 마다 이미지가 저장됨 -> 로컬에 저장된 모든 이미지 삭제
docker rmi $(docker images -q)

sudo git pull origin main

sudo docker build -t chanwkim/lovisbot:1.0.2 .

sudo docker push chanwkim/lovisbot:1.0.2

sudo docker run -dit chanwkim/lovisbot:1.0.2

echo "update complete!"