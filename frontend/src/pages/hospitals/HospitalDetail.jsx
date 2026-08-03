import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { client, apiError } from '../../api/client'
import { PageLoader } from '../../components/ui'

export default function HospitalDetail() {
  const { id } = useParams()
  const [hospital, setHospital] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    client
      .get(`/api/v1/hospitals/${id}`)
      .then((res) => setHospital(res.data))
      .catch((err) => setError(apiError(err, 'Hospital not found.')))
  }, [id])

  if (error) return <p className="card text-center text-red-600">{error}</p>
  if (!hospital) return <PageLoader />

  const mapsUrl = `https://www.google.com/maps?q=${hospital.latitude},${hospital.longitude}`

  return (
    <div className="mx-auto max-w-2xl space-y-6">
      <Link to="/hospitals" className="text-sm font-medium text-primary hover:underline">
        ← Back to hospitals
      </Link>
      <div className="card">
        <h1 className="text-2xl font-extrabold text-slate-900">{hospital.name}</h1>
        <p className="mt-1 text-sm text-slate-500">
          {hospital.city}
          {hospital.state ? `, ${hospital.state}` : ''}
          {hospital.pincode ? ` — ${hospital.pincode}` : ''}
        </p>
        {hospital.phone && (
          <a href={`tel:${hospital.phone.replace(/[^+\d]/g, '')}`} className="btn-outline mt-4 !py-2 text-sm">
            📞 {hospital.phone}
          </a>
        )}
      </div>

      <div className="card">
        <h2 className="font-bold text-slate-900">Address</h2>
        <p className="mt-2 text-sm text-slate-600">{hospital.address}</p>
        <a href={mapsUrl} target="_blank" rel="noreferrer" className="btn-outline mt-4 !py-2 text-sm">
          Open in Google Maps ↗
        </a>
      </div>

      {hospital.departments?.length > 0 && (
        <div className="card">
          <h2 className="font-bold text-slate-900">Departments</h2>
          <div className="mt-3 flex flex-wrap gap-2">
            {hospital.departments.map((d) => (
              <span key={d} className="rounded-lg bg-primary-50 px-3 py-1.5 text-xs font-semibold text-primary">
                {d}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
