[app]

# (str) Title of your application
title = BarberStyle

# (str) Package name
package.name = barberstyle

# (str) Package domain (needed for android/ios packaging)
package.domain = ru.int24

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,jpeg,ttf,md,kv,json

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec, ini

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = bin, .vscode, .gitignore, .buildozer

# (str) Application versioning (method 2)
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py
# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==1.11.1 , KivyMD==0.104.0, pillow, pygments, git+https://github.com/certifi/python-certifi.git
#,git+https://github.com/HeaTTheatR/KivyMD.git,pillow,pygments
# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
#requirements.source.kivymd = ../../kivymd
# (str) Presplash of the application
presplash.filename = %(source.dir)s/data/presplash.jpeg
# (str) Icon of the application
icon.filename = %(source.dir)s/data/kivy-icon.png
# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait
# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0
# (string) Presplash background color (for new android toolchain)
android.presplash_color = #FFFFFF
# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE
# (int) Target Android API, should be as high as possible.
android.api = 28
# (int) Minimum API your APK will support.
android.minapi = 21
# (str) Android NDK version to use
android.ndk = 19b
# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid excess Internet downloads or save time
# when an update is due and you just want to test/build your package
android.skip_update = False
# (bool) If True, then automatically accept SDK license
# agreements. This is intended for automation only. If set to False,
# the default, you will be shown the license when first running
# buildozer.
android.accept_sdk_license = True
# (str) Android logcat filters to use
android.logcat_filters = *:S python:D
# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = armeabi-v7a
[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2
# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0
# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = ./.buildozer
# (str) Path to build output (i.e. .apk, .ipa) storage
bin_dir = ./bin
#
