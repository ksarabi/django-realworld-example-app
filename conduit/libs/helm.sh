#!/bin/bash -x    
echo "inputs: $0,$1,$2"
cd conduit/libs
app=${1:-"app"}
chart=${2:-"bitnami/nginx"}
repo=`echo ${chart}| awk -F/ '{print $1}'`
#rm -f out.yaml
if [ "$repo" = "" ];then
  echo "Unable to get repo from chart:$chart"
  exit 1
fi

repoUrl=`curl -ks https://raw.githubusercontent.com/helm/hub/master/config/repo-values.yaml | grep -w ${repo} | grep url | awk '{print $NF}'`
if [ "$repoUrl" != "" ];then
    helm repo add ${repo} ${repoUrl}
else
    echo "Unable to find chart repo ${repo}"
    exit 1    
fi
if [ -f "values.json" ] ; then
  echo "helm template ${app} ${chart} -f values.json > out.yaml"
  if  ! helm template ${app} ${chart} -f values.json > out.yaml ; then
     #rm -f out.yaml
     echo "Unable to call helm"
     exit 1
  fi
else
  echo "Unable to find values.json"
  exit 1
fi