"use client"

import { useState } from "react"
import { useNavigate } from "react-router-dom"
import axios from "axios"
import { useTheme } from "./ThemeContext"

export default function Auth() {
  const [name, setName] = useState("")
  const [group, setGroup] = useState("")
  const [error, setError] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const navigate = useNavigate()
  const { isDarkMode } = useTheme()

  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setError(null)

    try {
      const response = await axios.post("http://127.0.0.1:8000/generate-task", {
        name,
        group,
      })

      const { imageId } = response.data
      navigate(`/task/${imageId}`)
    } catch (err) {
      setError(err.message || "Произошла ошибка при отправке данных")
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="auth-container">
      <h2>Авторизация</h2>
      <form onSubmit={handleSubmit}>
        <div className="question-group">
          <label htmlFor="name">Введите ФИО</label>
          <input
            type="text"
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="form-input"
            placeholder="Иванов Иван Иванович"
            required
            disabled={isLoading}
          />
        </div>
        <div className="question-group">
          <label htmlFor="group">Введите номер группы</label>
          <input
            type="text"
            id="group"
            value={group}
            onChange={(e) => setGroup(e.target.value)}
            className="form-input"
            placeholder="М8О-101БВ-24"
            required
            disabled={isLoading}
          />
        </div>
        {error && <div className="error-message">{error}</div>}
        <button type="submit" className="submit-button" disabled={isLoading}>
          {isLoading ? "Загрузка..." : "Продолжить"}
        </button>
      </form>
    </div>
  )
}
