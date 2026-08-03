import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { client, apiError, tokenStore } from '../../api/client'
import { useAuth } from '../../context/AuthContext'
import { Alert, Field, Modal, Spinner } from '../../components/ui'

export default function AccountSettings() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [pwForm, setPwForm] = useState({ current_password: '', new_password: '', confirm: '' })
  const [pwMsg, setPwMsg] = useState({ type: '', text: '' })
  const [pwLoading, setPwLoading] = useState(false)

  const [deleteOpen, setDeleteOpen] = useState(false)
  const [deletePassword, setDeletePassword] = useState('')
  const [deleteError, setDeleteError] = useState('')
  const [deleting, setDeleting] = useState(false)

  const changePassword = async (e) => {
    e.preventDefault()
    setPwMsg({ type: '', text: '' })
    if (pwForm.new_password !== pwForm.confirm) {
      setPwMsg({ type: 'error', text: 'New passwords do not match.' })
      return
    }
    setPwLoading(true)
    try {
      const { data } = await client.post('/api/v1/auth/change-password', {
        current_password: pwForm.current_password,
        new_password: pwForm.new_password,
      })
      // Change-password rotates tokens and invalidates other sessions.
      tokenStore.set(data.tokens)
      setPwForm({ current_password: '', new_password: '', confirm: '' })
      setPwMsg({ type: 'success', text: 'Password changed. All other sessions have been signed out.' })
    } catch (err) {
      setPwMsg({ type: 'error', text: apiError(err) })
    } finally {
      setPwLoading(false)
    }
  }

  const confirmDelete = async (e) => {
    e.preventDefault()
    setDeleteError('')
    setDeleting(true)
    try {
      await client.delete('/api/v1/users/me', { params: { password: deletePassword } })
      tokenStore.clear()
      window.dispatchEvent(new CustomEvent('carecode:logout'))
      navigate('/')
    } catch (err) {
      setDeleteError(apiError(err))
    } finally {
      setDeleting(false)
    }
  }

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900">Account settings</h1>
        <p className="text-sm text-slate-500">Manage your password and account.</p>
      </div>

      <form onSubmit={changePassword} className="card space-y-4">
        <h2 className="font-bold text-slate-900">Change password</h2>
        <Alert type={pwMsg.type}>{pwMsg.text}</Alert>
        <Field label="Current password">
          <input
            type="password"
            required
            autoComplete="current-password"
            className="input"
            value={pwForm.current_password}
            onChange={(e) => setPwForm({ ...pwForm, current_password: e.target.value })}
          />
        </Field>
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="New password" hint="8+ chars, upper & lower case, number, symbol">
            <input
              type="password"
              required
              autoComplete="new-password"
              className="input"
              value={pwForm.new_password}
              onChange={(e) => setPwForm({ ...pwForm, new_password: e.target.value })}
            />
          </Field>
          <Field label="Confirm new password">
            <input
              type="password"
              required
              autoComplete="new-password"
              className="input"
              value={pwForm.confirm}
              onChange={(e) => setPwForm({ ...pwForm, confirm: e.target.value })}
            />
          </Field>
        </div>
        <button type="submit" disabled={pwLoading} className="btn-primary">
          {pwLoading && <Spinner />} Change password
        </button>
      </form>

      <div className="card border-red-200 bg-red-50/50">
        <h2 className="font-bold text-red-700">Delete account</h2>
        <p className="mt-1 text-sm text-slate-600">
          Permanently deletes your account, medical profile, emergency contacts, photos, QR records and
          analytics. This action <strong className="text-red-700">cannot be undone</strong> — your QR code will
          stop working forever.
        </p>
        <button onClick={() => setDeleteOpen(true)} className="btn-danger mt-4">
          Delete account
        </button>
      </div>

      <Modal
        open={deleteOpen}
        onClose={() => setDeleteOpen(false)}
        title="Permanently delete your account?"
        footer={
          <>
            <button className="btn-ghost" onClick={() => setDeleteOpen(false)}>
              Cancel
            </button>
            <button className="btn-danger" onClick={confirmDelete} disabled={deleting}>
              {deleting && <Spinner />} Yes, delete forever
            </button>
          </>
        }
      >
        <div className="space-y-4">
          <Alert type="error">
            This is <strong>permanent and irreversible</strong>. All your personal and medical data will be
            deleted, and every QR code you have printed will become invalid immediately. To confirm, enter your
            password.
          </Alert>
          <Field label="Your password">
            <input
              type="password"
              required
              autoComplete="current-password"
              className="input"
              value={deletePassword}
              onChange={(e) => setDeletePassword(e.target.value)}
            />
          </Field>
          {deleteError && <Alert type="error">{deleteError}</Alert>}
        </div>
      </Modal>
    </div>
  )
}
