import { useState } from 'react'
import { Link, useNavigate, useSearchParams } from 'react-router-dom'
import { client, apiError } from '../../api/client'
import { Alert, Field, Spinner } from '../../components/ui'
import { passwordScore, strengthLabels, strengthColors } from '../../utils/format'

export default function ResetPassword() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const token = searchParams.get('token') || ''

  const [form, setForm] = useState({ password: '', confirm: '' })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [done, setDone] = useState(false)
  const score = passwordScore(form.password)

  const submit = async (e) => {
    e.preventDefault()
    setError('')
    if (!token) {
      setError('This reset link is invalid or has expired. Please request a new one.')
      return
    }
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
      await client.post('/api/v1/auth/reset-password', { token, password: form.password })
      setDone(true)
    } catch (err) {
      setError(apiError(err, 'This reset link is invalid or has expired.'))
    } finally {
      setLoading(false)
    }
  }

  if (done) {
    return (
      <div className="mx-auto mt-8 w-full max-w-md">
        <div className="card text-center">
          <div className="mx-auto mb-4 grid h-12 w-12 place-items-center rounded-full bg-emerald-100 text-2xl text-emerald-600">
            ✓
          </div>
          <h2 className="text-lg font-bold text-slate-900">Password updated</h2>
          <p className="mt-2 text-sm text-slate-600">
            Your password has been reset successfully. You can now log in with your new password.
          </p>
          <button onClick={() => navigate('/login')} className="btn-primary mt-6">
            Log in with new password
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="mx-auto mt-8 w-full max-w-md">
      <div className="mb-8 text-center">
        <h1 className="text-2xl font-extrabold text-slate-900">Set a new password</h1>
        <p className="mt-1 text-sm text-slate-500">Choose a strong password for your account.</p>
      </div>

      <form onSubmit={submit} className="card space-y-4">
        <Alert type="error">{error}</Alert>
        <Field label="New password" hint="8+ chars, upper & lower case, a number and a symbol.">
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
        <Field label="Confirm new password">
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
          {loading && <Spinner />} Reset password
        </button>
      </form>

      <p className="mt-6 text-center text-sm text-slate-600">
        <Link to="/login" className="font-semibold text-primary hover:underline">
          Back to login
        </Link>
      </p>
    </div>
  )
}
