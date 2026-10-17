[app]

# Название приложения
title = Accelerator Server

# Имя пакета
package.name = acceleratorserver

# Домен пакета
package.domain = org.accelerator

# Исходный код
source.dir = .

# Расширения файлов для включения в проект
source.include_exts = py,png,jpg,kv,atlas

# Версия приложения (обязательный параметр, на который ругался сборщик)
version = 1.0

# Список зависимостей
requirements = python3,kivy,socket,threading

# Ориентация экрана
orientation = portrait

# Права доступа для Android
android.permissions = INTERNET, ACCESS_WIFI_STATE, ACCESS_NETWORK_STATE, CHANGE_WIFI_STATE

# Версия API
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b

[buildozer]
log_level = 2
warn_on_root = 1
