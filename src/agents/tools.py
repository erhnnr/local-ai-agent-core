import datetime
import math

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
            # Sadece güvenli karakterlerin çalışmasına izin verelim
            allowed_chars = "0123456789+-*/(). "
            if not all(c in allowed_chars for c in expression):
                return "Hata: Geçersiz karakterler içeriyor."
            result = eval(expression)
            return str(result)
        except Exception as e:
            return f"Hesaplama hatası: {e}"

    @classmethod
    def execute_tool(cls, tool_name: str, argument: str) -> str:
        """Belirtilen aracı ismine göre çalıştırır."""
        if tool_name == "get_current_time":
            return cls.get_current_time()
        elif tool_name == "calculate_expression":
            return cls.calculate_expression(argument)
        else:
            return f"Bilinmeyen araç: {tool_name}"