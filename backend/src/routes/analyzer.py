from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import tempfile
from src.services.protocol_analyzer import ProtocolAnalyzer
from src.services.research_service import ResearchService

analyzer_bp = Blueprint('analyzer', __name__)

ALLOWED_EXTENSIONS = {'docx'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@analyzer_bp.route('/upload', methods=['POST'])
def upload_file():
    """Загрузка и анализ DOCX файла протокола"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Файл не найден'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Файл не выбран'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Разрешены только DOCX файлы'}), 400
        
        # Сохраняем файл во временную директорию
        filename = secure_filename(file.filename)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
            file.save(tmp_file.name)
            
            # Анализируем протокол
            analyzer = ProtocolAnalyzer()
            result = analyzer.analyze_protocol(tmp_file.name)
            
            # Удаляем временный файл
            os.unlink(tmp_file.name)
            
            return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': f'Ошибка при анализе: {str(e)}'}), 500

@analyzer_bp.route('/research/<drug_name>', methods=['GET'])
def search_research(drug_name):
    """Поиск исследований для конкретного препарата"""
    try:
        condition = request.args.get('condition', '')
        research_service = ResearchService()
        
        results = {
            'pubmed': research_service.search_pubmed(drug_name, condition),
            'clinical_trials': research_service.search_clinical_trials(drug_name, condition),
            'fda': research_service.search_fda(drug_name)
        }
        
        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': f'Ошибка при поиске исследований: {str(e)}'}), 500

@analyzer_bp.route('/export/pdf', methods=['POST'])
def export_pdf():
    """Экспорт результатов анализа в PDF"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Данные для экспорта не найдены'}), 400
        
        analyzer = ProtocolAnalyzer()
        pdf_path = analyzer.generate_pdf_report(data)
        
        return jsonify({'pdf_url': f'/api/download/{os.path.basename(pdf_path)}'})
    
    except Exception as e:
        return jsonify({'error': f'Ошибка при создании PDF: {str(e)}'}), 500

@analyzer_bp.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    """Скачивание сгенерированных файлов"""
    try:
        # Безопасная проверка имени файла
        filename = secure_filename(filename)
        downloads_dir = os.path.join(os.path.dirname(__file__), '..', 'downloads')
        
        if not os.path.exists(os.path.join(downloads_dir, filename)):
            return jsonify({'error': 'Файл не найден'}), 404
        
        return send_from_directory(downloads_dir, filename, as_attachment=True)
    
    except Exception as e:
        return jsonify({'error': f'Ошибка при скачивании: {str(e)}'}), 500

@analyzer_bp.route('/health', methods=['GET'])
def health_check():
    """Проверка состояния сервиса"""
    return jsonify({
        'status': 'healthy',
        'version': '2.0.0',
        'services': {
            'gemini_ai': True,  # TODO: добавить реальную проверку
            'pubmed': True,
            'clinical_trials': True,
            'fda': True
        }
    })

