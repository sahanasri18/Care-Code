import { useState } from 'react'
import { Link } from 'react-router-dom'
import { client, apiError } from '../../api/client'
import { Alert, Field, Spinner } from '../../components/ui'

export default function ForgotPassword() {
  const [email, setEmail] = useState('')
  const [sent, setSent] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const submit = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await client.post('/api/v1/auth/forgot-password', { email })
      setSent(true)
    } catch (err) {
      setError(apiError(err, 'Something went wrong. Please try again.'))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto mt-8 w-full max-w-md">
      <div className="mb-8 text-center">
        <h1 className="text-2xl font-extrabold text-slate-900">Forgot your password?</h1>
        <p className="mt-1 text-sm text-slate-500">
          Enter your registered email and we'll send you a reset link.
        </p>
      </div>

      {sent ? (
        <div className="card text-center">
          <div className="mx-auto mb-4 grid h-12 w-12 place-items-center rounded-full bg-emerald-100 text-2xl text-emerald-600">
            ✓
          </div>
          <h2 className="text-lg font-bold text-slate-900">Check your inbox</h2>
          <p className="mt-2 text-sm text-slate-600">
            If an account exists for <strong>{email}</strong>, a password reset link has been sent. The link is
            valid for 30 minutes and can be used only once.
          </p>
          <Link to="/login" className="btn-primary mt-6">
            Back to login
          </Link>
        </div>
      ) : (
        <form onSubmit={submit} className="card space-y-4">
          <Alert type="error">{error}</Alert>
          <Field label="Email address">
            <input
              type="email"
              required
              autoComplete="email"
              className="input"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </Field>
          <button type="submit" disabled={loading} className="btn-primary w-full">
            {loading && <Spinner />} Send reset link
          </button>
        </form>
      )}

      <p className="mt-6 text-center text-sm text-slate-600">
        Remembered it?{' '}
        <Link to="/login" className="font-semibold text-primary hover:underline">
          Back to login
        </Link>
      </p>
    </div>
  )
}
