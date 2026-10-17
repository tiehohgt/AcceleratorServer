import socket
import threading
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock

# Настройки сети
BROADCAST_PORT = 45001
TCP_PORT = 45000

class AcceleratorServerApp(App):
    def build(self):
        self.title = "Accelerator Server"
        self.server_active = False
        self.connected_device = "Нет подключений"

        # Основной контейнер с отступами
        layout = BoxLayout(orientation='vertical', padding=30, spacing=20)
        
        # Красивый фон (темная тема)
        with layout.canvas.before:
            Color(0.12, 0.12, 0.15, 1) # Темно-серый цвет
            self.bg_rect = Rectangle(size=(1000, 1000), pos=(0, 0))
        layout.bind(size=self._update_bg, pos=self._update_bg)

        # Заголовок
        self.header_label = Label(
            text="[b]Ускоритель (Сервер)[/b]",
            markup=True,
            font_size='22sp',
            size_hint=(1, 0.15),
            color=(0.9, 0.9, 1, 1)
        )
        layout.add_widget(self.header_label)

        # Информационное поле (Статус и подсказки для пользователя)
        self.status_label = Label(
            text="[color=ffaa00]Статус:[/color] Сервер выключен\n\n1. Включите точку доступа Wi-Fi на этом телефоне.\n2. Нажмите кнопку ниже для запуска сервера.",
            markup=True,
            font_size='16sp',
            halign='center',
            valign='middle',
            size_hint=(1, 0.4)
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        layout.add_widget(self.status_label)

        # Кнопка управления (Старт / Стоп)
        self.toggle_btn = Button(
            text="Запустить сервер",
            font_size='18sp',
            bold=True,
            size_hint=(1, 0.25),
            background_color=(0.2, 0.7, 0.3, 1) # Зеленая
        )
        self.toggle_btn.bind(on_press=self.toggle_server)
        layout.add_widget(self.toggle_btn)

        return layout

    def _update_bg(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def toggle_server(self, instance):
        if not self.server_active:
            self.server_active = True
            self.toggle_btn.text = "Остановить сервер"
            self.toggle_btn.background_color = (0.8, 0.2, 0.2, 1) # Красная
            self.status_label.text = "[color=00ff00]Статус:[/color] Сервер работает!\n\nОжидание подключения 32-битного устройства..."
            
            # Запускаем сетевые потоки
            threading.Thread(target=self.run_network_server, daemon=True).start()
        else:
            self.server_active = False
            self.toggle_btn.text = "Запустить сервер"
            self.toggle_btn.background_color = (0.2, 0.7, 0.3, 1)
            self.status_label.text = "[color=ffaa00]Статус:[/color] Сервер остановлен."

    def run_network_server(self):
        # 1. Поток автопоиска (Broadcast)
        threading.Thread(target=self.broadcast_loop, daemon=True).start()

        # 2. TCP сервер для команд
        self.tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.tcp_sock.bind(('0.0.0.0', TCP_PORT))
            self.tcp_sock.listen(5)
        except Exception as e:
            Clock.schedule_once(lambda dt: self.set_status_text(f"Ошибка сети: {e}"))
            return

        while self.server_active:
            try:
                self.tcp_sock.settimeout(1.0)
                conn, addr = self.tcp_sock.accept()
                ip = addr[0]
                Clock.schedule_once(lambda dt, i=ip: self.set_connected_status(i))
                
                data = conn.recv(1024).decode('utf-8').strip()
                if data:
                    print(f"Получена команда: {data}")
                    conn.sendall(b"STATUS:OK_EXECUTED")
                conn.close()
            except socket.timeout:
                continue
            except Exception:
                break
        
        try:
            self.tcp_sock.close()
        except:
            pass

    def broadcast_loop(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while self.server_active:
            try:
                s.sendto(b"ACCELERATOR_SERVER_HERE", ('<broadcast>', BROADCAST_PORT))
            except:
                pass
            time.sleep(1.0)
        s.close()

    def set_status_text(self, text):
        self.status_label.text = text

    def set_connected_status(self, ip):
        self.status_label.text = f"[color=00ff00]Статус:[/color] Устройство подключено!\n\nIP клиента: {ip}\nГотово к передаче команд."

if __name__ == '__main__':
    AcceleratorServerApp().run()
