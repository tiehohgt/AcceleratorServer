[app]

title = Accelerator Server
package.name = acceleratorserver
package.domain = org.accelerator

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy,socket,threading

orientation = portrait

android.permissions = INTERNET, ACCESS_WIFI_STATE, ACCESS_NETWORK_STATE, CHANGE_WIFI_STATE

# Фиксируем стабильные версии, чтобы сборщик не тянул проблемную 37-ю версию
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b
android.build_tools_version = 31.0.0

[buildozer]
log_level = 2
warn_on_root = 1
