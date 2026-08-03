import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { client, apiError } from '../../api/client'
import { PageLoader, Spinner } from '../../components/ui'

export default function Hospitals() {
  const [items, setItems] = useState([])
  const [cities, setCities] = useState([])
  const [states, setStates] = useState([])
  const [total, setTotal] = useState(0)
  const [q, setQ] = useState('')
  const [city, setCity] = useState('')
  const [state, setState] = useState('')
  const [page, setPage] = useState(1)
  const [nearby, setNearby] = useState(null)
  const [locating, setLocating] = useState(false)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const pageSize = 10

  const load = () => {
    setLoading(true)
    client
      .get('/api/v1/hospitals', {
        params: { q: q || undefined, city: city || undefined, state: state || undefined, page, page_size: pageSize },
      })
      .then((res) => {
        setItems(res.data.items)
        setTotal(res.data.total)
      })
      .catch((err) => setError(apiError(err)))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    client.get('/api/v1/hospitals/cities').then((res) => setCities(res.data.cities)).catch(() => {})
    client.get('/api/v1/hospitals/states').then((res) => setStates(res.data.states)).catch(() => {})
  }, [])

  useEffect(load, [q, city, state, page])

  const findNearby = () => {
    if (!navigator.geolocation) {
      setError('Geolocation is not supported by your browser.')
      return
    }
    setLocating(true)
    setError('')
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        client
          .get('/api/v1/hospitals/nearby', {
            params: { lat: pos.coords.latitude, lng: pos.coords.longitude, radius_km: 25 },
          })
          .then((res) => setNearby(res.data))
          .catch((err) => setError(apiError(err)))
          .finally(() => setLocating(false))
      },
      () => {
        setLocating(false)
        setError('Could not determine your location. Please allow location access.')
      }
    )
  }

  const list = nearby ?? items

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900">Find a hospital</h1>
        <p className="text-sm text-slate-500">Search our directory or find hospitals near you.</p>
      </div>

      <div className="card flex flex-col gap-3 sm:flex-row">
        <input
          className="input flex-1"
          placeholder="Search by name, city or address…"
          value={q}
          onChange={(e) => {
            setQ(e.target.value)
            setPage(1)
            setNearby(null)
          }}
        />
        <select
          className="input sm:w-48"
          value={city}
          onChange={(e) => {
            setCity(e.target.value)
            setPage(1)
            setNearby(null)
          }}
        >
          <option value="">All cities</option>
          {cities.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
        <select
          className="input sm:w-52"
          value={state}
          onChange={(e) => {
            setState(e.target.value)
            setCity('')
            setPage(1)
            setNearby(null)
          }}
        >
          <option value="">All states</option>
          {states.map((s) => (
            <option key={s} value={s}>
              {s}
            </option>
          ))}
        </select>
        <button onClick={findNearby} disabled={locating} className="btn-primary sm:w-48">
          {locating ? <Spinner /> : '📍 Nearby hospitals'}
        </button>
      </div>

      {error && <p className="text-sm text-red-600">{error}</p>}

      {nearby && (
        <p className="text-sm text-slate-600">
          Showing <strong>{nearby.length}</strong> hospitals within 25 km, sorted by distance. (
          <button className="font-semibold text-primary hover:underline" onClick={() => setNearby(null)}>
            show all
          </button>
          )
        </p>
      )}

      {loading ? (
        <PageLoader />
      ) : list.length === 0 ? (
        <p className="card text-center text-slate-500">No hospitals found.</p>
      ) : (
        <div className="grid gap-4 sm:grid-cols-2">
          {list.map((h) => (
            <Link key={h.id} to={`/hospitals/${h.id}`} className="card transition hover:border-primary hover:shadow-md">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <h2 className="font-bold text-slate-900">{h.name}</h2>
                  <p className="mt-0.5 text-sm text-slate-500">
                    {h.city}
                    {h.state ? `, ${h.state}` : ''}
                    {nearby ? ` · ${h.distance_km} km away` : ''}
                  </p>
                </div>
                <span className="shrink-0 rounded-lg bg-primary-50 px-2 py-1 text-xs font-semibold text-primary">
                  {h.departments?.[0] || 'General'}
                </span>
              </div>
              {h.phone && <p className="mt-3 text-sm font-medium text-slate-700">{h.phone}</p>}
            </Link>
          ))}
        </div>
      )}

      {!nearby && total > pageSize && (
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
    </div>
  )
}
