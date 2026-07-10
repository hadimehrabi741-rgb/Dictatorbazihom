[app]
title = Boundless AI
package.name = boundlessai
package.domain = org.boundless

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf
source.exclude_dirs = .github, .buildozer, attached_assets, storage/backups, storage/distributed_backups

version = 1.0.1

# Requirements: added arabic-reshaper for proper Persian/Arabic shaping
requirements = python3,kivy,pyjnius,requests,certifi,urllib3,charset-normalizer,idna,python-bidi,arabic-reshaper

orientation = portrait
fullscreen = 0

# Permissions: include storage permissions (requested at runtime in the app)
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# Compile & target SDK: set to a recent Android SDK to avoid Play Protect warnings
android.api = 34
android.target = 34
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a
android.build_tools_version = 33.0.2
android.enable_androidx = True
android.logcat_filters = *:S python:D

presplash.filename = %(source.dir)s/assets/presplash.png
icon.filename = %(source.dir)s/assets/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
