"use client"

import { useParams, useNavigate } from "react-router-dom"
import { useState, useEffect } from "react"
import { useTheme } from "./ThemeContext"

export default function Result() {
  const { imageId } = useParams()
  const navigate = useNavigate()
  const [resultData, setResultData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [image, setImage] = useState(null)
  const [taskData, setTaskData] = useState(null)
  const [answers, setAnswers] = useState({})
  const { isDarkMode } = useTheme()

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        setError(null)

        // Загружаем результаты
        const resultResponse = await fetch(`http://localhost:8000/result/${imageId}`)
        if (!resultResponse.ok) throw new Error("Результаты не найдены")
        const result = await resultResponse.json()
        setResultData(result)

        // Загружаем сохраненные ответы
        const savedAnswers = localStorage.getItem(`task_${imageId}_answers`)
        if (savedAnswers) {
          setAnswers(JSON.parse(savedAnswers))
        }

        // Загружаем изображение
        const imageResponse = await fetch(`http://localhost:8000/img/${imageId}`)
        if (!imageResponse.ok) throw new Error("Изображение не найдено")
        const imageBlob = await imageResponse.blob()
        setImage(URL.createObjectURL(imageBlob))

        // Загружаем данные задачи
        const taskResponse = await fetch(`http://localhost:8000/task/${imageId}`)
        if (!taskResponse.ok) throw new Error("Задание не найдено")
        const data = await taskResponse.json()
        setTaskData(data)
      } catch (err) {
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [imageId])

  const handleTryAgain = () => {
    navigate(`/`)
  }

  const getQuestions = () => {
    if (!taskData) return []

    return [
      {
        id: "q1",
        text: `Класс эквивалентности [x]ρ, где x = ${Math.round(taskData.y_2)}:`,
        type: "text",
      },
      {
        id: "q2",
        text: `Класс эквивалентности [x]ρ, где x ∈ (${taskData.start_x_3}; ${taskData.end_x_3}):`,
        type: "text",
      },
      {
        id: "q3",
        text: `Класс эквивалентности [x]ρ, где x ∈ ${taskData.correct_more}:`,
        type: "text",
      },
    ]
  }

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Загрузка результатов...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="error-container">
        <h2>Ошибка</h2>
        <p>{error}</p>
        <button className="submit-button" onClick={() => navigate("/")}>
          Вернуться на главную
        </button>
      </div>
    )
  }

  const isAllCorrect = resultData.result_1 && resultData.result_2 && resultData.result_3

  return (
    <>
      <div className="page-header">
        <h1>
          Функция f(x) определяет отношение ρ на множестве
          <br />Х = [0;5]: x₁ρх₂ ⇔ f(x₁) = f(x₂).
        </h1>
      </div>
      <div className="app-container">
        <div className="image-container">
          <img src={image || "/placeholder.svg"} alt="График функции" />
        </div>
        <div className="form-container">
          <div style={{ textAlign: "center", marginBottom: "30px" }}>
            <h2>Результаты</h2>
            <h3 className={isAllCorrect ? "correct" : "incorrect"}>
              {isAllCorrect ? "Молодец! Все правильно" : "Неверно. Попробуйте еще раз"}
            </h3>
            <div
              style={{
                margin: "20px 0",
                padding: "15px",
                borderRadius: "var(--border-radius)",
                backgroundColor: "var(--background-color)",
              }}
            >
              <p>
                <strong>ФИО:</strong> {resultData.name}
              </p>
              <p>
                <strong>Группа:</strong> {resultData.group}
              </p>
              <p>
                <strong>Время начала:</strong> {resultData.start}
                <br />
                <strong>Время окончания:</strong> {resultData.finish}
              </p>
              <p>
                <strong>Время решения:</strong> {Math.floor(resultData.solving / 60)} мин.{" "}
                {(resultData.solving % 60).toFixed(2)} сек.
              </p>
            </div>
          </div>

          <h3>Ваши ответы:</h3>
          <form>
            {getQuestions().map((question, index) => (
              <div key={question.id} className="question-group">
                <div className="result-item">
                  {resultData[`result_${question.id.slice(1)}`] ? (
                    <span className="result-icon correct">✓</span>
                  ) : (
                    <span className="result-icon incorrect">✗</span>
                  )}
                  <label htmlFor={`question-${question.id}`}>{question.text}</label>
                </div>
                <input
                  type={question.type}
                  id={`question-${question.id}`}
                  value={answers[question.id] || ""}
                  className="form-input"
                  readOnly
                />
              </div>
            ))}
          </form>

          <button onClick={handleTryAgain} className="submit-button">
            Решить еще раз
          </button>
        </div>
      </div>
    </>
  )
}
