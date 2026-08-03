import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { client, apiError, absoluteUrl } from '../../api/client'
import { Spinner } from '../../components/ui'
import { ageFromDob } from '../../utils/format'

function Section({ title, children, danger }) {
  if (!children) return null
  return (
    <section className="rounded-2xl bg-white p-4 shadow-sm">
      <h2 className={`text-xs font-extrabold uppercase tracking-widest ${danger ? 'text-danger' : 'text-primary'}`}>
        {title}
      </h2>
      <div className="mt-2 whitespace-pre-wrap text-[15px] leading-relaxed text-slate-800">{children}</div>
    </section>
  )
}

export default function EmergencyPage() {
  const { code } = useParams()
  const [data, setData] = useState(null)
  const [gone, setGone] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => {
    client
      .get(`/api/v1/public/${code}`)
      .then((res) => setData(res.data))
      .catch((err) => {
        if (err.response?.status === 410) setGone(true)
        else setError(apiError(err))
      })
  }, [code])

  if (gone) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center bg-slate-50 px-4">
        <div className="grid h-16 w-16 place-items-center rounded-full bg-slate-200 text-3xl text-slate-500">⚠</div>
        <h1 className="mt-6 text-xl font-extrabold text-slate-900">CareCode profile unavailable</h1>
        <p className="mt-3 max-w-sm text-center text-sm leading-relaxed text-slate-600">
          This CareCode profile is no longer available. The owner has deleted or deactivated this emergency
          profile.
        </p>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="flex min-h-screen flex-col items-center justify-center bg-slate-50">
        {error ? <p className="text-sm text-red-600">{error}</p> : <Spinner className="h-10 w-10 text-primary" />}
      </div>
    )
  }

  const hasAllergies = Boolean(data.allergies)
  const hasConditions = Boolean(data.conditions)

  return (
    <div className="min-h-screen bg-slate-100 pb-10">
      <div className="bg-danger px-4 py-3 text-center text-xs font-bold uppercase tracking-widest text-white">
        Emergency medical profile · CareCode
      </div>

      <div className="mx-auto mt-4 w-full max-w-md space-y-3 px-4">
        <header className="flex items-center gap-4 rounded-2xl bg-white p-4 shadow-sm">
          {data.photo_url ? (
            <img src={absoluteUrl(data.photo_url)} alt={data.full_name} className="h-20 w-20 rounded-2xl object-cover" />
          ) : (
            <div className="grid h-20 w-20 place-items-center rounded-2xl bg-primary-50 text-3xl font-extrabold text-primary">
              {data.full_name.charAt(0).toUpperCase()}
            </div>
          )}
          <div>
            <h1 className="text-xl font-extrabold text-slate-900">{data.full_name}</h1>
            <p className="mt-0.5 text-sm text-slate-500">
              {[data.age ? `Age ${data.age}` : null, data.gender && data.gender !== 'prefer not to say' ? data.gender : null]
                .filter(Boolean)
                .join(' · ') || 'Age not provided'}
            </p>
            {data.blood_group && (
              <span className="mt-2 inline-block rounded-lg bg-red-50 px-2.5 py-1 text-sm font-extrabold text-danger ring-1 ring-danger/20">
                Blood group {data.blood_group}
              </span>
            )}
          </div>
        </header>

        {(hasAllergies || hasConditions) && (
          <div className="rounded-2xl border-2 border-danger bg-red-50/70 p-3 text-xs font-semibold text-danger">
            <strong>Medical alert:</strong>{' '}
            {[hasAllergies && 'allergies', hasConditions && 'conditions'].filter(Boolean).join(' & ')} recorded below
          </div>
        )}

        <Section title="Allergies" danger>{data.allergies}</Section>
        <Section title="Medical conditions" danger>{data.conditions}</Section>
        <Section title="Current medications">{data.medications}</Section>

        {data.contacts?.length > 0 && (
          <section className="rounded-2xl bg-white p-4 shadow-sm">
            <h2 className="text-xs font-extrabold uppercase tracking-widest text-primary">Emergency contacts</h2>
            <div className="mt-3 space-y-2.5">
              {data.contacts.map((c, i) => (
                <div key={i} className="flex items-center justify-between gap-3">
                  <div className="min-w-0">
                    <p className="truncate text-sm font-semibold text-slate-800">{c.name}</p>
                    <p className="text-xs text-slate-500">{c.relationship}</p>
                  </div>
                  <a href={`tel:${c.phone.replace(/[^+\d]/g, '')}`} className="btn-primary shrink-0 !rounded-full !px-4 !py-2 text-xs">
                    📞 Call
                  </a>
                </div>
              ))}
            </div>
          </section>
        )}

        <Section title="Address">{data.address}</Section>
        <Section title="Important notes">{data.notes}</Section>

        <a
          href={absoluteUrl(`/api/v1/public/${code}/summary`)}
          className="btn-outline w-full justify-center"
          download
        >
          Download medical summary
        </a>

        <p className="pt-2 text-center text-[11px] text-slate-400">
          CareCode — Scan. Care. Save Lives.
        </p>
      </div>
    </div>
  )
}
