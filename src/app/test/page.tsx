'use client'
import React, { useEffect } from 'react'

const TestPage = () => {
  const fetchData = async () => {
    const response = await fetch("http://localhost:8888/test")
    const data = await response.json()
    console.log(data)
  }
  
  useEffect(() => {
    
    console.log("test")
    fetchData()
  })
  
  return (
    <div>
      <h1>Test Page</h1>
      
    </div>
  )
}

export default TestPage