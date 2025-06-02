import { BrowserRouter, Routes, Route } from "react-router-dom"
import { ThemeProvider } from "./ThemeContext"
import ThemeToggle from "./components/ThemeToggle"
import Auth from "./Auth.jsx"
import Task from "./Task.jsx"
import Result from "./Result.jsx"
import "./styles/global.css"

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <ThemeToggle />
        <Routes>
          <Route path="/" element={<Auth />} />
          <Route path="/task/:imageId" element={<Task />} />
          <Route path="/result/:imageId" element={<Result />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  )
}
