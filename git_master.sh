#!/usr/bin/env bash
# 保存当前目录
currentDir=$PWD
echo "Start to publish...\n"
# 切换到项目目录
echo  $1
echo "\n"


if [[ $1 = 'test' ]];
then
        cd  /builds/summer815288/test/
        # 执行git命令
        git  checkout master
        git pull origin master
        git merge sim
        git push origin master

elif [[ $1 = 'sd_teemo' ]];
then
         cd /var/www/sd_teemo/
        # 执行git命令
        git pull origin sim
else
  echo "Input Is Error."
fi


# 切换回原来的目录
cd $currentDir
# 删除缓存

echo "Success\n";
