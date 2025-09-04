import { useState } from 'react'
import { Upload, FileText, Search, Download, AlertCircle, CheckCircle } from 'lucide-react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Alert, AlertDescription } from '@/components/ui/alert.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [analysisResult, setAnalysisResult] = useState(null)
  const [error, setError] = useState(null)
  const [progress, setProgress] = useState(0)

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0]
    if (selectedFile && selectedFile.name.endsWith('.docx')) {
      setFile(selectedFile)
      setError(null)
      setAnalysisResult(null)
    } else {
      setError('Пожалуйста, выберите файл в формате DOCX')
      setFile(null)
    }
  }

  const analyzeProtocol = async () => {
    if (!file) return

    setIsAnalyzing(true)
    setError(null)
    setProgress(0)

    try {
      const formData = new FormData()
      formData.append('file', file)

      // Симуляция прогресса
      const progressInterval = setInterval(() => {
        setProgress(prev => Math.min(prev + 10, 90))
      }, 500)

      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData
      })

      clearInterval(progressInterval)
      setProgress(100)

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Ошибка при анализе файла')
      }

      const result = await response.json()
      setAnalysisResult(result)
    } catch (err) {
      setError(err.message)
    } finally {
      setIsAnalyzing(false)
      setTimeout(() => setProgress(0), 1000)
    }
  }

  const searchResearch = async (drugName, condition) => {
    try {
      const params = new URLSearchParams()
      if (condition) params.append('condition', condition)
      
      const response = await fetch(`/api/research/${encodeURIComponent(drugName)}?${params}`)
      if (response.ok) {
        return await response.json()
      }
    } catch (err) {
      console.error('Ошибка при поиске исследований:', err)
    }
    return null
  }

  const exportToPDF = async () => {
    if (!analysisResult) return

    try {
      const response = await fetch('/api/export/pdf', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(analysisResult)
      })

      if (response.ok) {
        const result = await response.json()
        window.open(result.pdf_url, '_blank')
      }
    } catch (err) {
      setError('Ошибка при экспорте в PDF')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="container mx-auto max-w-6xl">
        {/* Header */}
        <div className="text-center py-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Анализатор клинических протоколов
          </h1>
          <p className="text-gray-600 mb-1">
            Современная система анализа с интеграцией медицинских баз данных
          </p>
          <p className="text-sm text-gray-500">
            Загрузите DOCX файл для автоматического анализа с поиском исследований
          </p>
        </div>

        {/* Upload Section */}
        <Card className="mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileText className="h-5 w-5" />
              Загрузка протокола
            </CardTitle>
            <CardDescription>
              Выберите DOCX файл клинического протокола для анализа
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center space-x-4">
                <input
                  type="file"
                  accept=".docx"
                  onChange={handleFileChange}
                  className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer"
                  disabled={isAnalyzing}
                />
                {file && (
                  <span className="text-sm text-green-600 flex items-center gap-1">
                    <CheckCircle className="h-4 w-4" />
                    {file.name}
                  </span>
                )}
              </div>
              
              {progress > 0 && (
                <div className="space-y-2">
                  <Progress value={progress} className="w-full" />
                  <p className="text-sm text-gray-600 text-center">
                    Анализ протокола... {progress}%
                  </p>
                </div>
              )}

              <Button
                onClick={analyzeProtocol}
                disabled={!file || isAnalyzing}
                className="w-full"
                size="lg"
              >
                {isAnalyzing ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Анализируем...
                  </>
                ) : (
                  <>
                    <Search className="h-4 w-4 mr-2" />
                    Начать анализ протокола
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Error Display */}
        {error && (
          <Alert variant="destructive" className="mb-6">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Results Section */}
        {analysisResult && (
          <Card className="mb-6">
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                <span className="flex items-center gap-2">
                  <CheckCircle className="h-5 w-5 text-green-500" />
                  Результаты анализа
                </span>
                <Button onClick={exportToPDF} variant="outline" size="sm">
                  <Download className="h-4 w-4 mr-2" />
                  Экспорт в PDF
                </Button>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Alert className="mb-4 border-amber-200 bg-amber-50">
                <AlertCircle className="h-4 w-4 text-amber-600" />
                <AlertDescription className="text-amber-800">
                  <strong>Внимание:</strong> Анализ генерируется искусственным интеллектом. 
                  Эта информация предназначена для ознакомительных целей и не заменяет 
                  консультацию квалифицированного медицинского специалиста.
                </AlertDescription>
              </Alert>

              {/* Protocol Summary */}
              {analysisResult.protocol_summary && (
                <div className="mb-6 p-4 bg-gray-50 rounded-lg">
                  <h3 className="text-lg font-semibold text-gray-700 mb-2">
                    Резюме протокола
                  </h3>
                  <p className="text-gray-600 whitespace-pre-line">
                    {analysisResult.protocol_summary}
                  </p>
                  {analysisResult.main_condition && (
                    <p className="text-sm text-gray-500 mt-2">
                      <strong>Основное состояние:</strong> {analysisResult.main_condition}
                    </p>
                  )}
                </div>
              )}

              {/* Drugs Analysis */}
              {analysisResult.drugs && analysisResult.drugs.length > 0 && (
                <div className="space-y-4">
                  <h3 className="text-lg font-semibold text-gray-700">
                    Анализ лекарственных средств
                  </h3>
                  {analysisResult.drugs.map((drug, index) => (
                    <Card key={index} className="border-l-4 border-l-blue-500">
                      <CardContent className="pt-4">
                        <h4 className="text-lg font-bold text-blue-700 mb-2">
                          {drug.name || 'Название не указано'}
                        </h4>
                        {drug.innEnglish && (
                          <p className="text-sm text-gray-600 italic mb-2">
                            МНН (англ.): {drug.innEnglish}
                          </p>
                        )}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                          <div>
                            <strong>Дозировка:</strong> {drug.dosage || 'Не указано'}
                          </div>
                          <div>
                            <strong>Путь введения:</strong> {drug.route || 'Не указано'}
                          </div>
                          <div>
                            <strong>Режим:</strong> {drug.frequency || 'Не указано'}
                          </div>
                          <div>
                            <strong>Длительность:</strong> {drug.duration || 'Не указано'}
                          </div>
                        </div>
                        {drug.indication && (
                          <div className="mt-2 text-sm">
                            <strong>Показание:</strong> {drug.indication}
                          </div>
                        )}
                      </CardContent>
                    </Card>
                  ))}
                </div>
              )}

              {(!analysisResult.drugs || analysisResult.drugs.length === 0) && (
                <div className="text-center py-8 text-gray-500">
                  Не удалось извлечь информацию о лекарствах из документа. 
                  Попробуйте другой документ или проверьте его содержимое.
                </div>
              )}
            </CardContent>
          </Card>
        )}

        {/* Footer */}
        <footer className="text-center py-8 text-sm text-gray-500 border-t border-gray-200">
          <p>&copy; {new Date().getFullYear()} Анализатор клинических протоколов. Модульная версия.</p>
          <p>Технологии: React, Flask, Tailwind CSS, Gemini AI, PubMed API</p>
        </footer>
      </div>
    </div>
  )
}

export default App

