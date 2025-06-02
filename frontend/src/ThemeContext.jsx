"use client"

import { createContext, useContext, useState, useEffect } from "react"

const ThemeContext = createContext()

export function ThemeProvider({ children }) {
  const [isDarkMode, setIsDarkMode] = useState(() => {
    // Check if user has a saved preference
    const savedTheme = localStorage.getItem("theme")
    return savedTheme === "dark" || (!savedTheme && window.matchMedia("(prefers-color-scheme: dark)").matches)
  })

  useEffect(() => {
    // Update localStorage and apply theme to document
    localStorage.setItem("theme", isDarkMode ? "dark" : "light")
    document.documentElement.classList.toggle("dark-mode", isDarkMode)
  }, [isDarkMode])

  const toggleTheme = () => {
    setIsDarkMode((prev) => !prev)
  }

  return <ThemeContext.Provider value={{ isDarkMode, toggleTheme }}>{children}</ThemeContext.Provider>
}

export function useTheme() {
  return useContext(ThemeContext)
}
