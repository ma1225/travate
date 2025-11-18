import React from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

export default function Results() {
  const { state } = useLocation()
  const navigate = useNavigate()

  if (!state) {
    return (
      <div className="container py-5">
        <div className="alert alert-warning">No results to display. Please submit your trip first.</div>
        <button className="btn btn-primary" onClick={() => navigate('/')}>Go to Home</button>
      </div>
    )
  }

  const { selection, joiners } = state

  return (
    <div className="container py-5">
      <h2 className="text-center mb-4">Your travel selections</h2>

      <div className="table-responsive">
        <table className="table table-bordered table-striped">
          <thead className="table-dark">
            <tr>
              <th>Travel date</th>
              <th>Preferences</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{selection.travelDate || '—'}</td>
              <td>{(selection.preferences || []).join(', ') || '—'}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <h3 className="mt-5">Users willing to join solo travelers</h3>

      <div className="table-responsive">
        <table className="table table-hover">
          <thead className="table-primary">
            <tr>
              <th>Gender</th>
              <th>Name</th>
              <th>Country</th>
              <th>Age</th>
              <th>Interest</th>
              <th>Bio</th>
            </tr>
          </thead>
          <tbody>
            {joiners?.length ? (
              joiners.map((u, idx) => (
                <tr key={idx}>
                  <td>{u.gender}</td>
                  <td>{u.name}</td>
                  <td>{u.country}</td>
                  <td>{u.age}</td>
                  <td>{u.interest}</td>
                  <td>{u.bio}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="5" className="text-center text-muted">No joiners found at the moment.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      <div className="d-flex gap-2 mt-4">
        <button className="btn btn-outline-secondary" onClick={() => navigate('/')}>Back</button>
        <button className="btn btn-primary" onClick={() => navigate('/')}>Plan another trip</button>
      </div>
    </div>
  )
}
