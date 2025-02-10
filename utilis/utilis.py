class FormatedText:
    
    @staticmethod
    def formatMarkdownV2(text: str) -> str:

        replacements = {
            '_': r'\_', '[': r'\[', ']': r'\]', '(': r'\(', ')': r'\)',
            '~': r'\~', '`': r'\`', '>': r'\>', '#': r'\#', '+': r'\+',
            '-': r'\-', '=': r'\=', '|': r'\|', '{': r'\{', '}': r'\}',
            '.': r'\.', '!': r'\!'
        }
        
        for symbol, replacement in replacements.items():
            text = text.replace(symbol, replacement)
    
        return text
    
class SenderMessages:
    @staticmethod
    async def replyMessage(message,keyboard):
        pass