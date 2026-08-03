import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import { apiError } from '../../api/client'
import { Alert, Field, Spinner } from '../../components/ui'
import { passwordScore, strengthLabels, strengthColors } from '../../utils/format'

export default function Register() {
  const { register } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({ full_name: '', email: '', password: '', confirm: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const score = passwordScore(form.password)

  const submit = async (e) => {
    e.preventDefault()
    setError('')
    if (form.password !== form.confirm) {
      setError('Passwords do not match.')
      return
    }
    if (score < 3) {
      setError('Password is too weak. Use at least 8 characters with upper & lower case, a number and a symbol.')
      return
    }
    setLoading(true)
    try {
      await register({ full_name: form.full_name, email: form.email, password: form.password })
      navigate('/dashboard')
    } catch (err) {
      setError(apiError(err, 'Unable to create your account.'))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto mt-8 w-full max-w-md">
      <div className="mb-8 text-center">
        <h1 className="text-2xl font-extrabold text-slate-900">Create your account</h1>
        <p className="mt-1 text-sm text-slate-500">Your emergency medical profile could save your life.</p>
      </div>

      <form onSubmit={submit} className="card space-y-4">
        <Alert type="error">{error}</Alert>
        <Field label="Full name">
          <input
            type="text"
            required
            minLength={2}
            autoComplete="name"
            className="input"
            value={form.full_name}
            onChange={(e) => setForm({ ...form, full_name: e.target.value })}
          />
        </Field>
        <Field label="Email address">
          <input
            type="email"
            required
            autoComplete="email"
            className="input"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
          />
        </Field>
        <Field label="Password" hint="8+ chars, upper & lower case, a number and a symbol.">
          <input
            type="password"
            required
            autoComplete="new-password"
            className="input"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
          />
          {form.password && (
            <div className="mt-2">
              <div className="flex gap-1">
                {[1, 2, 3, 4].map((i) => (
                  <div
                    key={i}
                    className={`h-1.5 flex-1 rounded-full ${i <= score ? strengthColors[score] : 'bg-slate-200'}`}
                  />
                ))}
              </div>
              <p className="mt-1 text-xs text-slate-500">{strengthLabels[score]}</p>
            </div>
          )}
        </Field>
        <Field label="Confirm password">
          <input
            type="password"
            required
            autoComplete="new-password"
            className="input"
            value={form.confirm}
            onChange={(e) => setForm({ ...form, confirm: e.target.value })}
          />
        </Field>
        <button type="submit" disabled={loading} className="btn-primary w-full">
          {loading && <Spinner />} Create account
        </button>
      </form>

      <p className="mt-6 text-center text-sm text-slate-600">
        Already have an account?{' '}
        <Link to="/login" className="font-semibold text-primary hover:underline">
          Log in
        </Link>
      </p>
    </div>
  )
}
