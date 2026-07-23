import datetime
import os

class ToolRegistry:
    """
    Yapay zeka modelinin çağırabileceği araçların (fonksiyonların) 
    kayıtlı olduğu ve yönetildiği sınıf.
    """
    @staticmethod
    def get_current_time() -> str:
        """Sistemdeki anı ve tarihi döndürür."""
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def calculate_expression(expression: str) -> str:
        """Güvenli temel matematiksel hesaplamalar yapar."""
        try:
            allowed_chars = "0123456789+-*/(). "
            if not all(c in allowed_chars for c in expression):
                return "Hata: Geçersiz karakterler içeriyor."
            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"Hesaplama hatası: {e}"

    @staticmethod
    def read_local_file(file_path: str) -> str:
        """Proje dizinindeki bir metin veya kod dosyasının içeriğini okur."""
        try:
            # Güvenlik için sadece proje klasörü içi veya güvenli yollar denetlenebilir
            if not os.path.exists(file_path):
                return f"Hata: '{file_path}' dosyası bulunamadı."
            
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            # Çok uzun dosyalar için kırpma yapılabilir
            return content[:3000] + ("\n[...dosya uzantısı kırpıldı...]" if len(content) > 3000 else "")
        except Exception as e:
            return f"Dosya okuma hatası: {e}"

    @classmethod
    def execute_tool(cls, tool_name: str, argument: str) -> str:
        """Belirtilen aracı ismine göre çalıştırır."""
        if tool_name == "get_current_time":
            return cls.get_current_time()
        elif tool_name == "calculate_expression":
            return cls.calculate_expression(argument)
        elif tool_name == "read_local_file":
            return cls.read_local_file(argument)
        else:
            return f"Bilinmeyen araç: {tool_name}"