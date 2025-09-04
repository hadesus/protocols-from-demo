import os
import json
import tempfile
from typing import Dict, List, Any
import mammoth
import google.generativeai as genai
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch

class ProtocolAnalyzer:
    def __init__(self):
        """Инициализация анализатора протоколов"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY не найден в переменных окружения")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def extract_text_from_docx(self, file_path: str) -> str:
        """Извлечение текста из DOCX файла"""
        try:
            with open(file_path, 'rb') as docx_file:
                result = mammoth.extract_raw_text(docx_file)
                return result.value
        except Exception as e:
            raise Exception(f"Ошибка при извлечении текста из DOCX: {str(e)}")
    
    def analyze_protocol(self, file_path: str) -> Dict[str, Any]:
        """Основной метод анализа протокола"""
        try:
            # Извлекаем текст из документа
            text = self.extract_text_from_docx(file_path)
            
            if not text.strip():
                raise Exception("Документ пуст или не содержит текста")
            
            # Анализируем протокол с помощью ИИ
            analysis_result = self._analyze_with_ai(text)
            
            return {
                'success': True,
                'protocol_summary': analysis_result.get('protocolSummary', ''),
                'main_condition': analysis_result.get('mainCondition', ''),
                'drugs': analysis_result.get('drugs', []),
                'analysis_timestamp': self._get_timestamp()
            }
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'analysis_timestamp': self._get_timestamp()
            }
    
    def _analyze_with_ai(self, text: str) -> Dict[str, Any]:
        """Анализ текста с помощью Gemini AI"""
        prompt = f"""
Проанализируйте следующий клинический протокол и извлеките информацию о лекарственных средствах.

Текст протокола:
{text}

Верните результат в JSON формате:
{{
  "protocolSummary": "краткое резюме протокола",
  "mainCondition": "основное заболевание или состояние",
  "drugs": [
    {{
      "id": "уникальный идентификатор",
      "name": "название препарата",
      "innEnglish": "международное непатентованное название на английском",
      "innRussian": "международное непатентованное название на русском", 
      "dosage": "дозировка",
      "route": "путь введения",
      "frequency": "режим приема",
      "duration": "длительность",
      "indication": "показание к применению из протокола",
      "targetCondition": "конкретное заболевание/состояние для поиска исследований"
    }}
  ]
}}

Важно: 
- Для innEnglish используйте точное международное непатентованное название (INN) на английском языке
- Для targetCondition укажите наиболее специфичное заболевание или состояние
- Если препарат не найден, не включайте его в список
"""
        
        try:
            response = self.model.generate_content(prompt)
            
            # Извлекаем JSON из ответа
            response_text = response.text
            
            # Ищем JSON в ответе
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise Exception("Не удалось найти JSON в ответе ИИ")
            
            json_text = response_text[start_idx:end_idx]
            result = json.loads(json_text)
            
            return result
        
        except json.JSONDecodeError as e:
            raise Exception(f"Ошибка при парсинге JSON ответа: {str(e)}")
        except Exception as e:
            raise Exception(f"Ошибка при анализе с помощью ИИ: {str(e)}")
    
    def generate_pdf_report(self, analysis_data: Dict[str, Any]) -> str:
        """Генерация PDF отчета"""
        try:
            # Создаем временный файл для PDF
            downloads_dir = os.path.join(os.path.dirname(__file__), '..', 'downloads')
            os.makedirs(downloads_dir, exist_ok=True)
            
            pdf_filename = f"protocol_analysis_{self._get_timestamp()}.pdf"
            pdf_path = os.path.join(downloads_dir, pdf_filename)
            
            # Создаем PDF документ
            doc = SimpleDocTemplate(pdf_path, pagesize=letter)
            styles = getSampleStyleSheet()
            story = []
            
            # Заголовок
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1  # Центрирование
            )
            story.append(Paragraph("Анализ клинического протокола", title_style))
            story.append(Spacer(1, 12))
            
            # Общая информация
            if analysis_data.get('protocol_summary'):
                story.append(Paragraph("Резюме протокола:", styles['Heading2']))
                story.append(Paragraph(analysis_data['protocol_summary'], styles['Normal']))
                story.append(Spacer(1, 12))
            
            if analysis_data.get('main_condition'):
                story.append(Paragraph("Основное состояние:", styles['Heading2']))
                story.append(Paragraph(analysis_data['main_condition'], styles['Normal']))
                story.append(Spacer(1, 12))
            
            # Таблица препаратов
            if analysis_data.get('drugs'):
                story.append(Paragraph("Анализ лекарственных средств:", styles['Heading2']))
                
                # Создаем данные для таблицы
                table_data = [['Препарат', 'МНН (англ.)', 'Дозировка', 'Путь введения', 'Режим']]
                
                for drug in analysis_data['drugs']:
                    table_data.append([
                        drug.get('name', ''),
                        drug.get('innEnglish', ''),
                        drug.get('dosage', ''),
                        drug.get('route', ''),
                        drug.get('frequency', '')
                    ])
                
                # Создаем таблицу
                table = Table(table_data, colWidths=[1.5*inch, 1.5*inch, 1*inch, 1*inch, 1*inch])
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(table)
            
            # Генерируем PDF
            doc.build(story)
            
            return pdf_path
        
        except Exception as e:
            raise Exception(f"Ошибка при генерации PDF: {str(e)}")
    
    def _get_timestamp(self) -> str:
        """Получение текущего времени в формате строки"""
        from datetime import datetime
        return datetime.now().strftime("%Y%m%d_%H%M%S")

