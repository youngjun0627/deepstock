#!/bin/sh


# ps -ef을 이용해서 원하는 프로세스 정보를 얻는다.
process=$(ps -ef | grep 'python3 main.py$')


pid=$(echo ${process} | cut -d " " -f2)


if [ -n "${pid}" ]
then
        result=$(kill -9 ${pid})
        echo process is killed.
else
        echo running process not found.
fi

