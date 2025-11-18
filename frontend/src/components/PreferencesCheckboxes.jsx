import React from 'react'

export default function PreferencesCheckboxes({ value = [], onChange, options = [] }) {
  const toggle = (opt) => {
    if (value.includes(opt)) {
      onChange(value.filter(v => v !== opt))
    } else {
      onChange([...value, opt])
    }
  }

  return (
    <div className="d-flex flex-wrap gap-3">
      {options.map((opt) => (
        <div className="form-check form-check-inline" key={opt}>
          <input
            className="form-check-input"
            type="checkbox"
            id={`pref-${opt}`}
            checked={value.includes(opt)}
            onChange={() => toggle(opt)}
          />
          <label className="form-check-label" htmlFor={`pref-${opt}`}>{opt}</label>
        </div>
      ))}
    </div>
  )
}
