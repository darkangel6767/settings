#!/bin/bash

if [[ ! -d platforms ]]
  then
  echo "Directory 'platforms' is not found"
  exit 1
fi
resfile=App_Resources/Android/src/main/res/values/strings.xml
apkname=$(basename $PWD)
if [[ ! -f $resfile || ! -s $resfile ]]
  then
  read -p 'display app name: ' displayname
  cat <<EOF > $(basename $resfile)
<?xml version="1.0" encoding="utf-8"?>
<resources>
  <string name="app_name">$displayname</string>
  <string name="title_activity_kimera">$apkname</string>
</resources>
EOF
  cp $(basename $resfile) $(dirname $resfile)/
fi
sd '(?P<filters>abiFilters) .* (?P<arch>.arm64-v8a.)' '$filters $arch' platforms/android/app/build.gradle
ver=$(grep version package.json | awk '{print $2}' | sd ',' '')
sd '(versionName) (".+")' "\$1 $ver" App_Resources/Android/app.gradle
ns build android --release   --key-store-path ~/.config/key0-keystore.jks   --key-store-password genome6767   --key-store-alias key0   --key-store-alias-password genome6767   --apk   --copy-to dist/$apkname.apk
