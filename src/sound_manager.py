import json
import pathlib

import arcade


class SoundManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        self.sounds = {}
        self.sound_enabled = True
        self.settings_path = pathlib.Path(__file__).parent / "settings.json"

        self.load_settings()
        self.load_sounds()

    def load_settings(self):
        """Загружает JSON"""
        try:
            if self.settings_path.exists():
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.sound_enabled = data.get("sound_effects", True)
        except Exception as e:
            print(f"SoundManager: ошибка загрузки настроек: {e}")
            self.sound_enabled = True

    def save_settings(self):
        """Сохраняет в JSON"""
        try:
            data = {}
            if self.settings_path.exists():
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

            data["sound_effects"] = self.sound_enabled

            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"SoundManager: ошибка сохранения настроек: {e}")

    def load_sounds(self):
        """Загружает все файлы"""
        base_path = pathlib.Path(__file__).parent.parent / "assets" / "sounds"

        sound_files = {
            "jump": "jump.wav",
            "death": "death.wav",
            "button_press": "button_press.ogg",
            "door_open": "door_open.ogg",
            "ui_click": "click.mp3",
        }

        for sound_name, filename in sound_files.items():
            sound_path = base_path / filename
            try:
                if sound_path.exists():
                    self.sounds[sound_name] = arcade.load_sound(sound_path)
                else:
                    print(f"SoundManager: файла нету! - {sound_path}")
                    self.sounds[sound_name] = None
            except Exception as e:
                print(f"SoundManager: ошибка загрузки {filename}: {e}")
                self.sounds[sound_name] = None

    def play(self, sound_name: str, volume: float = 1.0):
        """Воспроизводит звук по имени"""
        if not self.sound_enabled:
            return

        sound = self.sounds.get(sound_name)
        if sound:
            try:
                arcade.play_sound(sound, volume=volume)
            except Exception as e:
                print(f"SoundManager: ошибка воспроизведения {sound_name}: {e}")

    def play_jump(self):
        self.play("jump", 0.5)

    def play_death(self):
        self.play("death", 0.7)

    def play_button_press(self):
        self.play("button_press", 0.6)

    def play_door_open(self):
        self.play("door_open", 0.5)

    def play_ui_click(self):
        self.play("ui_click", 0.4)

    def toggle_sound(self) -> bool:
        """Переключает звук и возвращает новое состояние"""
        self.sound_enabled = not self.sound_enabled
        self.save_settings()
        return self.sound_enabled

    def set_enabled(self, enabled: bool):
        """Устанавливает состояние звука"""
        self.sound_enabled = enabled
        self.save_settings()


sound_manager = SoundManager()
