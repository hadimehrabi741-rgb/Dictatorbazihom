[app]
title = Boundless AI
package.name = boundlessai
package.domain = org.boundless

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json

version = 1.0.0

requirements = python3==3.11,kivy==2.3.0,requests,certifi,openssl

orientation = portrait

fullscreen = 0

android.permissions = INTERNET

android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33
android.ndk_api = 21

android.archs = arm64-v8a

# Use Gradle 8
android.gradle_dependencies =

android.enable_androidx = True

android.logcat_filters = *:S python:D

presplash.filename = %(source.dir)s/assets/presplash.png
icon.filename = %(source.dir)s/assets/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
