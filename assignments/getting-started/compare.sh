#!/bin/bash 

for j in out emr-out; do 
  echo concatenating and sorting entries in $j
  cd $j
  echo > temp
  echo > temp.sorted
  for i in `ls part-*`; do 
    cat $i >> temp ;
  done
  cat temp | sort > temp.sorted
  echo " found `cat temp.sorted | wc -l` tags"
  cd ..
done
diff -qs out/temp.sorted emr-out/temp.sorted 
rm */temp */temp.sorted 
