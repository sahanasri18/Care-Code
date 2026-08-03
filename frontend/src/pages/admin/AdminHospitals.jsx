import { useEffect, useState } from 'react'
import { client, apiError } from '../../api/client'
import { Alert, Field, Modal, PageLoader, Spinner } from '../../components/ui'

const EMPTY = { name: '', address: '', city: '', state: '', pincode: '', phone: '', latitude: '', longitude: '', departments: '' }

export default function AdminHospitals() {
  const [items, setItems] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [q, setQ] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [editing, setEditing] = useState(null) // null | 'new' | hospital
  const [form, setForm] = useState(EMPTY)
  const [saving, setSaving] = useState(false)
  const pageSize = 10

  const load = () => {
    setLoading(true)
    client
      .get('/api/v1/admin/hospitals', { params: { q: q || undefined, page, page_size: pageSize } })
      .then((res) => {
        setItems(res.data.items)
        setTotal(res.data.total)
      })
      .catch((err) => setError(apiError(err)))
      .finally(() => setLoading(false))
  }
  useEffect(load, [q, page])

  const openNew = () => {
    setForm(EMPTY)
    setEditing('new')
  }
  const openEdit = (h) => {
    setForm({
      name: h.name,
      address: h.address,
      city: h.city,
      state: h.state,
      pincode: h.pincode || '',
      phone: h.phone || '',
      latitude: h.latitude,
      longitude: h.longitude,
      departments: (h.departments || []).join(', '),
    })
    setEditing(h)
  }

  const save = async (e) => {
    e.preventDefault()
    setSaving(true)
    setError('')
    const payload = {
      ...form,
      latitude: parseFloat(form.latitude),
      longitude: parseFloat(form.longitude),
      departments: form.departments
        .split(',')
        .map((d) => d.trim())
        .filter(Boolean),
    }
    try {
      if (editing === 'new') await client.post('/api/v1/admin/hospitals', payload)
      else await client.put(`/api/v1/admin/hospitals/${editing.id}`, payload)
      setEditing(null)
      load()
    } catch (err) {
      setError(apiError(err))
    } finally {
      setSaving(false)
    }
  }

  const remove = async (h) => {
    if (!window.confirm(`Delete ${h.name}? This cannot be undone.`)) return
    try {
      await client.delete(`/api/v1/admin/hospitals/${h.id}`)
      load()
    } catch (err) {
      setError(apiError(err))
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900">Hospital management</h1>
          <p className="text-sm text-slate-500">{total} hospitals in the directory</p>
        </div>
        <div className="flex gap-2">
          <input
            className="input sm:w-64"
            placeholder="Search hospitals…"
            value={q}
            onChange={(e) => {
              setQ(e.target.value)
              setPage(1)
            }}
          />
          <button className="btn-primary !py-2 text-xs" onClick={openNew}>
            + Add hospital
          </button>
        </div>
      </div>

      <Alert type="error">{error}</Alert>

      {loading ? (
        <PageLoader />
      ) : (
        <div className="card overflow-x-auto !p-0">
          <table className="w-full min-w-[640px] text-left text-sm">
            <thead>
              <tr className="border-b border-slate-200 text-xs uppercase tracking-wide text-slate-400">
                <th className="px-4 py-3">Name</th>
                <th className="px-4 py-3">City</th>
                <th className="px-4 py-3">Phone</th>
                <th className="px-4 py-3">Departments</th>
                <th className="px-4 py-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {items.map((h) => (
                <tr key={h.id} className="hover:bg-slate-50">
                  <td className="max-w-[220px] px-4 py-3">
                    <p className="truncate font-semibold text-slate-900">{h.name}</p>
                    <p className="truncate text-xs text-slate-500">{h.address}</p>
                  </td>
                  <td className="px-4 py-3">
                    <p className="font-semibold text-slate-900">{h.city}</p>
                    <p className="text-xs text-slate-500">{h.state}</p>
                  </td>
                  <td className="px-4 py-3 text-xs">{h.phone || '—'}</td>
                  <td className="px-4 py-3 text-xs text-slate-500">{(h.departments || []).slice(0, 2).join(', ')}</td>
                  <td className="px-4 py-3">
                    <div className="flex justify-end gap-2">
                      <button className="btn-outline !px-3 !py-1.5 text-xs" onClick={() => openEdit(h)}>
                        Edit
                      </button>
                      <button className="btn-danger !px-3 !py-1.5 text-xs" onClick={() => remove(h)}>
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {total > pageSize && (
        <div className="flex justify-center gap-2">
          <button className="btn-outline" disabled={page === 1} onClick={() => setPage(page - 1)}>
            Previous
          </button>
          <span className="flex items-center px-3 text-sm text-slate-600">
            Page {page} of {Math.ceil(total / pageSize)}
          </span>
          <button className="btn-outline" disabled={page >= Math.ceil(total / pageSize)} onClick={() => setPage(page + 1)}>
            Next
          </button>
        </div>
      )}

      <Modal
        open={Boolean(editing)}
        onClose={() => setEditing(null)}
        title={editing === 'new' ? 'Add hospital' : `Edit — ${editing?.name}`}
        footer={
          <>
            <button className="btn-ghost" onClick={() => setEditing(null)}>
              Cancel
            </button>
            <button className="btn-primary" onClick={save} disabled={saving}>
              {saving && <Spinner />} Save
            </button>
          </>
        }
      >
        <form onSubmit={save} className="space-y-3">
          <Field label="Name *">
            <input className="input" required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
          </Field>
          <Field label="Address *">
            <input className="input" required value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} />
          </Field>
          <div className="grid grid-cols-2 gap-3">
            <Field label="City *">
              <input className="input" required value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} />
            </Field>
            <Field label="State *">
              <input className="input" required value={form.state} onChange={(e) => setForm({ ...form, state: e.target.value })} />
            </Field>
            <Field label="Pincode">
              <input className="input" value={form.pincode} onChange={(e) => setForm({ ...form, pincode: e.target.value })} />
            </Field>
            <Field label="Phone">
              <input className="input" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
            </Field>
            <Field label="Latitude *">
              <input className="input" required type="number" step="any" value={form.latitude} onChange={(e) => setForm({ ...form, latitude: e.target.value })} />
            </Field>
            <Field label="Longitude *">
              <input className="input" required type="number" step="any" value={form.longitude} onChange={(e) => setForm({ ...form, longitude: e.target.value })} />
            </Field>
          </div>
          <Field label="Departments (comma separated)">
            <input className="input" value={form.departments} onChange={(e) => setForm({ ...form, departments: e.target.value })} />
          </Field>
        </form>
      </Modal>
    </div>
  )
}
