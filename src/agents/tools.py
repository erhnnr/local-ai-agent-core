import platform
from datetime import datetime
import json
import urllib.request
import psutil


class ToolRegistry:
    """Ajanın kullanabileceği tüm araçların (tools) kayıt ve yürütme merkezi."""
    
    @staticmethod
    def execute_tool(tool_name: str, arg: str = "") -> str:
        if tool_name == "get_current_time":
            return ToolRegistry.get_current_time()
        elif tool_name == "read_local_file":
            return ToolRegistry.read_local_file(arg)
        elif tool_name == "get_system_info":
            return ToolRegistry.get_system_info()
        elif tool_name == "get_weather":
            return ToolRegistry.get_weather(arg)
        return f"Hata: '{tool_name}' adında bir araç bulunamadı."

    @staticmethod
    def get_current_time() -> str:
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def read_local_file(filepath: str) -> str:
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Dosya okuma hatası: {e!s}"

    @staticmethod
    def get_system_info() -> str:
        """Bilgisayarın işletim sistemi ve temel donanım/bellek bilgilerini döndürür."""
        try:
            uname = platform.uname()
            mem = psutil.virtual_memory()
            info = (
                f"İşletim Sistemi: {uname.system} {uname.release} ({uname.version})\n"
                f"Bilgisayar Adı: {uname.node}\n"
                f"İşlemci (CPU): {uname.processor}\n"
                f"Toplam RAM: {round(mem.total / (1024.3 ** 3), 2)} GB\n"
                f"Kullanılan RAM Oranı: %{mem.percent}"
            )
            return info
        except Exception as e:
            return f"Sistem bilgisi alınırken hata oluştu: {e!s}"

    @staticmethod
    def get_weather(city: str = "Antalya") -> str:
        """Belirtilen şehir için anlık hava durumu bilgisini internet üzerinden çeker."""
        try:
            url = f"https://wttr.in/{city}?format=j1"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode('utf-8'))
                current = data['current_condition'][0]
                temp = current['temp_C']
                desc = current['weatherDesc'][0]['value']
                return f"Şehir: {city}\nSıcaklık: {temp}°C\nDurum: {desc}"
        except Exception as e:
            return f"Hava durumu alınamadı: {e!s}"