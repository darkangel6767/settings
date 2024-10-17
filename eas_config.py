#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import subprocess

eas_obj = {
    "build": {
        "preview": {
            "android": {
                "buildType": "apk"
            }
        },
        "preview2": {
            "android": {
                "gradleCommand": ":app:assembleRelease"
            }
        },
        "preview3": {
            "developmentClient": True
        },
        "preview4": {
            "distribution": "internal"
        },
        "production": {}
    }
}
eas_file = 'eas.json'
app_props = {
    "expo": {
        "plugins": [
            [
                "expo-build-properties",
                {
                    "android": {
                        "enableProguardInReleaseBuilds": True,
                        "enableShrinkResourcesInReleaseBuilds": True,
                        "useLegacyPackaging": True
                    },
                }
            ]
        ]
    }
}
app_file = 'app.json'
app_obj = None
install_plugin = False

with open(app_file) as f:
    app_obj = json.load(f)
plugins = app_obj['expo'].get('plugins', [])
has_prop = False
for idx, pl in enumerate(plugins):
    if isinstance(pl, list) and pl[0] == 'expo-build-properties':
        has_prop = True
        break
if has_prop:
    plugins[idx][1]['android'] = app_props['expo']['plugins'][0][1]['android']
else:
    plugins.append(app_props['expo']['plugins'][0])
    install_plugin = True
app_obj['expo']['plugins'] = plugins
with open(app_file, 'w+') as f:
    json.dump(app_obj, f, indent=2)
with open(eas_file, 'w+') as f:
    json.dump(eas_obj, f, indent=2)
if install_plugin:
    subprocess.run(['npm', 'i', 'expo-build-properties'])
print('done')
