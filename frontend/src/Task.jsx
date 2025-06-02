"use client"

import { useParams, useNavigate } from "react-router-dom"
import { useState, useEffect } from "react"
import { useTheme } from "./ThemeContext"

export default function Task() {
  const { imageId } = useParams()
  const navigate = useNavigate()
  const [taskData, setTaskData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [image, setImage] = useState(null)
  const [answers, setAnswers] = useState({})
  const [submitting, setSubmitting] = useState(false)
  const { isDarkMode } = useTheme()

  // Сохраняем ответы в localStorage при их изменении
  useEffect(() => {
    if (Object.keys(answers).length > 0) {
      localStorage.setItem(`task_${imageId}_answers`, JSON.stringify(answers))
    }
  }, [answers, imageId])

  // Загружаем сохраненные ответы и данные задачи
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        setError(null)

        // Загружаем сохраненные ответы (если есть)
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

  const getQuestions = () => {
    if (!taskData) return []

    return [
      {
        id: "q1",
        text: `Указать класс эквивалентности [x]ρ, где x = ${Math.round(taskData.y_2)}:`,
        type: "text",
        hint: "Пример ответа: [a;b]U{c;d}\n(a,b,c,d - числа)",
      },
      {
        id: "q2",
        text: `Указать класс эквивалентности [x]ρ, где x ∈ (${taskData.start_x_3}; ${taskData.end_x_3}):`,
        type: "text",
        hint: "Пример ответа: [a;b]U{c;d}\n(a,b,c,d - числа)",
      },
      {
        id: "q3",
        text: `Указать класс эквивалентности [x]ρ, где x = ${taskData.correct_more}:`,
        type: "text",
        hint: "Пример ответа: [a;b]U{c;d}\n(a,b,c,d - числа)",
      },
    ]
  }

  const handleInputChange = (questionId, value) => {
    setAnswers((prev) => ({
      ...prev,
      [questionId]: value,
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setSubmitting(true)

    try {
      const response = await fetch(`http://localhost:8000/answers/${imageId}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(answers),
      })

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)

      // Перенаправляем на страницу результатов (без очистки localStorage)
      navigate(`/result/${imageId}`)
    } catch (error) {
      console.error("Ошибка отправки:", error)
      alert(`Ошибка: ${error.message}`)
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return (
      <div className="loading-container">
        <div className="loading-spinner"></div>
        <p>Загрузка задания...</p>
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
          <h2>Составить ответ используя символы: U, <i>x</i>, [, ], {'{, }'}, цифры 0-9</h2>
          <h2>Вопросы</h2>
          <form onSubmit={handleSubmit}>
            {getQuestions().map((question) => (
              <div key={question.id} className="question-group">
                <label htmlFor={`question-${question.id}`} className="question-label">
                  {question.text}
                  <span className="tooltip">
                    ?<span className="tooltip-text">{question.hint}</span>
                  </span>
                </label>
                <input
                  type={question.type}
                  id={`question-${question.id}`}
                  value={answers[question.id] || ""}
                  onChange={(e) => handleInputChange(question.id, e.target.value)}
                  className="form-input"
                  disabled={submitting}
                />
              </div>
            ))}
            <button type="submit" className="submit-button" disabled={submitting}>
              {submitting ? "Отправка..." : "Ответить"}
            </button>
          </form>
        </div>
      </div>
    </>
  )
}
