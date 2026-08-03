import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { client, apiError, absoluteUrl } from '../../api/client'
import { Alert, Field, PageLoader, Spinner } from '../../components/ui'

const BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
const GENDERS = ['male', 'female', 'other', 'prefer not to say']

const EMPTY_CONTACT = { name: '', relationship: '', phone: '' }

export default function ProfileEditor() {
  const navigate = useNavigate()
  const [form, setForm] = useState(null)
  const [photoUrl, setPhotoUrl] = useState(null)
  const [saving, setSaving] = useState(false)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  useEffect(() => {
    client
      .get('/api/v1/users/me/profile')
      .then((res) => {
        const p = res.data
        setForm({
          full_name: p.full_name,
          date_of_birth: p.date_of_birth || '',
          gender: p.gender || '',
          blood_group: p.blood_group || '',
          allergies: p.allergies || '',
          conditions: p.conditions || '',
          medications: p.medications || '',
          address: p.address || '',
          notes: p.notes || '',
          contacts: p.contacts.length ? p.contacts : [EMPTY_CONTACT],
        })
        setPhotoUrl(p.photo_url ? absoluteUrl(p.photo_url) : null)
      })
      .catch((err) => setError(apiError(err)))
  }, [])

  const update = (key, value) => setForm({ ...form, [key]: value })
  const updateContact = (i, key, value) => {
    const contacts = form.contacts.map((c, idx) => (idx === i ? { ...c, [key]: value } : c))
    update('contacts', contacts)
  }

  const submit = async (e) => {
    e.preventDefault()
    setSaving(true)
    setError('')
    setSuccess('')
    try {
      const payload = {
        ...form,
        date_of_birth: form.date_of_birth || null,
        gender: form.gender || null,
        blood_group: form.blood_group || null,
        contacts: form.contacts
          .filter((c) => c.name.trim() && c.phone.trim())
          .map((c) => ({ name: c.name.trim(), relationship: c.relationship.trim() || 'Contact', phone: c.phone.trim() })),
      }
      const { data } = await client.post('/api/v1/users/me/profile', payload)
      setForm({ ...form, contacts: data.contacts })
      setSuccess('Profile saved successfully.')
    } catch (err) {
      setError(apiError(err))
    } finally {
      setSaving(false)
    }
  }

  const uploadPhoto = async (file) => {
    setUploading(true)
    setError('')
    try {
      const fd = new FormData()
      fd.append('file', file)
      const { data } = await client.post('/api/v1/users/me/profile/photo', fd, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      setPhotoUrl(absoluteUrl(data.photo_url))
      setSuccess('Photo uploaded.')
    } catch (err) {
      setError(apiError(err, 'Photo must be JPEG, PNG or WebP under 5 MB.'))
    } finally {
      setUploading(false)
    }
  }

  const removePhoto = async () => {
    try {
      const { data } = await client.delete('/api/v1/users/me/profile/photo')
      setPhotoUrl(null)
      setSuccess('Photo removed.')
    } catch (err) {
      setError(apiError(err))
    }
  }

  if (!form) return <PageLoader />

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900">Emergency medical profile</h1>
        <p className="text-sm text-slate-500">
          This information appears on your public emergency page when your QR is scanned.
        </p>
      </div>

      <form onSubmit={submit} className="card space-y-5">
        <Alert type="error">{error}</Alert>
        <Alert type="success">{success}</Alert>

        <div className="flex items-center gap-4">
          {photoUrl ? (
            <img src={photoUrl} alt="Profile" className="h-20 w-20 rounded-full object-cover" />
          ) : (
            <div className="grid h-20 w-20 place-items-center rounded-full bg-primary-50 text-2xl font-bold text-primary">
              {form.full_name.charAt(0).toUpperCase()}
            </div>
          )}
          <div className="flex flex-wrap gap-2">
            <label className="btn-outline cursor-pointer !py-1.5 text-xs">
              {uploading ? <Spinner className="h-4 w-4" /> : 'Upload photo'}
              <input
                type="file"
                accept="image/jpeg,image/png,image/webp"
                className="hidden"
                onChange={(e) => e.target.files[0] && uploadPhoto(e.target.files[0])}
              />
            </label>
            {photoUrl && (
              <button type="button" onClick={removePhoto} className="btn-ghost !py-1.5 text-xs">
                Remove
              </button>
            )}
          </div>
        </div>

        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Full name *">
            <input className="input" required value={form.full_name} onChange={(e) => update('full_name', e.target.value)} />
          </Field>
          <Field label="Date of birth">
            <input
              type="date"
              className="input"
              value={form.date_of_birth}
              max={new Date().toISOString().split('T')[0]}
              onChange={(e) => update('date_of_birth', e.target.value)}
            />
          </Field>
          <Field label="Gender">
            <select className="input" value={form.gender} onChange={(e) => update('gender', e.target.value)}>
              <option value="">Prefer not to say</option>
              {GENDERS.map((g) => (
                <option key={g} value={g}>
                  {g}
                </option>
              ))}
            </select>
          </Field>
          <Field label="Blood group">
            <select className="input" value={form.blood_group} onChange={(e) => update('blood_group', e.target.value)}>
              <option value="">Not specified</option>
              {BLOOD_GROUPS.map((b) => (
                <option key={b} value={b}>
                  {b}
                </option>
              ))}
            </select>
          </Field>
        </div>

        <Field label="Allergies" hint="e.g. Penicillin — severe reaction">
          <textarea rows={2} className="input" value={form.allergies} onChange={(e) => update('allergies', e.target.value)} />
        </Field>
        <Field label="Medical conditions" hint="e.g. Type 1 Diabetes, Asthma">
          <textarea rows={2} className="input" value={form.conditions} onChange={(e) => update('conditions', e.target.value)} />
        </Field>
        <Field label="Current medications" hint="e.g. Insulin 20u daily">
          <textarea rows={2} className="input" value={form.medications} onChange={(e) => update('medications', e.target.value)} />
        </Field>
        <div className="grid gap-4 sm:grid-cols-2">
          <Field label="Address">
            <textarea rows={2} className="input" value={form.address} onChange={(e) => update('address', e.target.value)} />
          </Field>
          <Field label="Important notes" hint="e.g. Carries glucagon kit">
            <textarea rows={2} className="input" value={form.notes} onChange={(e) => update('notes', e.target.value)} />
          </Field>
        </div>

        <div>
          <h2 className="mb-2 font-bold text-slate-900">Emergency contacts</h2>
          <p className="mb-4 text-xs text-slate-500">
            Responders can call these numbers instantly from your public page.
          </p>
          <div className="space-y-3">
            {form.contacts.map((c, i) => (
              <div key={i} className="grid gap-3 rounded-xl border border-slate-200 bg-slate-50 p-3 sm:grid-cols-[1fr_1fr_1fr_auto]">
                <input
                  className="input"
                  placeholder="Name"
                  value={c.name}
                  onChange={(e) => updateContact(i, 'name', e.target.value)}
                />
                <input
                  className="input"
                  placeholder="Relationship"
                  value={c.relationship}
                  onChange={(e) => updateContact(i, 'relationship', e.target.value)}
                />
                <input
                  className="input"
                  placeholder="Phone"
                  value={c.phone}
                  onChange={(e) => updateContact(i, 'phone', e.target.value)}
                />
                <button
                  type="button"
                  className="btn-ghost !px-3"
                  onClick={() => update('contacts', form.contacts.filter((_, idx) => idx !== i))}
                  disabled={form.contacts.length === 1}
                  aria-label="Remove contact"
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
          <button
            type="button"
            className="btn-outline mt-3 !py-1.5 text-xs"
            onClick={() => update('contacts', [...form.contacts, EMPTY_CONTACT])}
          >
            + Add contact
          </button>
        </div>

        <div className="flex items-center gap-3 border-t border-slate-100 pt-5">
          <button type="submit" disabled={saving} className="btn-primary">
            {saving && <Spinner />} Save profile
          </button>
          <button type="button" onClick={() => navigate('/dashboard')} className="btn-ghost">
            Cancel
          </button>
        </div>
      </form>
    </div>
  )
}
