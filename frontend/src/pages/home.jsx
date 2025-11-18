import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import PreferencesCheckboxes from '../components/PreferencesCheckboxes.jsx'

export default function Home() {
  const navigate = useNavigate()
  const [travelDate, setTravelDate] = useState('')
  const [preferences, setPreferences] = useState([])

  const handleSubmit = async (e) => {
    e.preventDefault()
    const payload = { travelDate, preferences }
    const res = await fetch('http://localhost:5000/api/plan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    })
    const data = await res.json()
    navigate('/results', { state: data })
  }

  return (
    <div className="home-page bg-image text-white d-flex align-items-center">
      <div className="container py-5">
        <nav className="navbar navbar-dark">
          <span className="navbar-brand h1">🌍 Travel Mate AI</span>
          <div>
            <a className="btn btn-outline-light me-2" href="#how">How it works</a>
            <a className="btn btn-outline-light" href="#about">About</a>
          </div>
        </nav>

        <div className="row justify-content-center mt-4">
          <div className="col-12 col-md-8 col-lg-6">
            <div className="card bg-dark bg-opacity-75 shadow-lg">
              <div className="card-body">
                <h2 className="card-title mb-3">Plan your trip and meet new friends</h2>
                <form onSubmit={handleSubmit}>
                  <div className="mb-3">
                    <label htmlFor="travelDate" className="form-label">Travel date</label>
                    <input
                      type="date"
                      id="travelDate"
                      className="form-control"
                      value={travelDate}
                      onChange={(e) => setTravelDate(e.target.value)}
                      required
                    />
                  </div>

                  <div className="mb-3">
                    <label className="form-label">Vacation preferences</label>
                    <PreferencesCheckboxes
                      value={preferences}
                      onChange={setPreferences}
                      options={['Popular Attractions', 'Bars', 'Restaurants']}
                    />
                  </div>

                  <button type="submit" className="btn btn-primary btn-lg w-100">
                      Submit for the best traveling experience you will encounter
                  </button>
                </form>
              </div>
            </div>
            <div id="how" className="text-white-50 mt-3">
              <p className="mb-0">Enter your dates and preferences, we’ll match your plan and show friendly solo joiners.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
