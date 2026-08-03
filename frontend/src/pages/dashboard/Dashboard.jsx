import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { client, apiError, absoluteUrl } from '../../api/client'
import { useAuth } from '../../context/AuthContext'
import { PageLoader, StatCard } from '../../components/ui'
import { formatDateTime } from '../../utils/format'

export default function Dashboard() {
  const { user } = useAuth()
  const [profile, setProfile] = useState(null)
  const [stats, setStats] = useState(null)
  const [activity, setActivity] = useState([])
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      client.get('/api/v1/users/me/profile'),
      client.get('/api/v1/analytics/me'),
      client.get('/api/v1/analytics/me/activity?limit=10'),
    ])
      .then(([p, s, a]) => {
        setProfile(p.data)
        setStats(s.data)
        setActivity(a.data)
      })
      .catch((err) => setError(apiError(err)))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <PageLoader />

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-extrabold text-slate-900">Welcome, {user.full_name.split(' ')[0]}</h1>
        <p className="text-sm text-slate-500">Here's how your CareCode is doing.</p>
      </div>

      <div className="grid gap-4 sm:grid-cols-3">
        <StatCard label="Total scans" value={stats?.total_scans ?? 0} sub="Times your QR was viewed" />
        <StatCard label="Scans (30 days)" value={stats?.scans_last_30_days ?? 0} sub="Recent activity" />
        <StatCard
          label="Last scanned"
          value={stats?.last_scanned_at ? formatDateTime(stats.last_scanned_at).split(',')[0] : 'Never'}
          sub={stats?.last_scanned_at ? formatDateTime(stats.last_scanned_at) : 'Scan your QR to test it'}
        />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <section className="card">
          <div className="mb-4 flex items-center justify-between">
            <h2 className="font-bold text-slate-900">Emergency profile</h2>
            <Link to="/profile" className="btn-outline !py-1.5 text-xs">
              Edit profile
            </Link>
          </div>
          {profile ? (
            <div className="flex items-center gap-4">
              <div className="grid h-14 w-14 place-items-center rounded-full bg-primary-50 text-xl font-bold text-primary">
                {profile.full_name.charAt(0).toUpperCase()}
              </div>
              <div>
                <p className="font-semibold text-slate-900">{profile.full_name}</p>
                <p className="text-sm text-slate-500">
                  {[profile.blood_group && `Blood ${profile.blood_group}`, profile.gender, profile.allergies && 'Has allergies']
                    .filter(Boolean)
                    .join(' · ') || 'Profile details pending'}
                </p>
              </div>
            </div>
          ) : (
            <p className="text-sm text-slate-500">No profile yet.</p>
          )}
          <div className="mt-4 flex gap-2">
            <Link to="/qr" className="btn-outline flex-1 justify-center text-xs">
              View / download QR
            </Link>
          </div>
        </section>

        <section className="card">
          <h2 className="mb-4 font-bold text-slate-900">Recent activity</h2>
          {activity.length === 0 ? (
            <p className="text-sm text-slate-500">No activity yet.</p>
          ) : (
            <ul className="divide-y divide-slate-100">
              {activity.map((a, i) => (
                <li key={i} className="flex items-center justify-between py-2.5 text-sm">
                  <span className="capitalize text-slate-700">{a.action.replace(/_/g, ' ')}</span>
                  <span className="text-xs text-slate-400">{formatDateTime(a.created_at)}</span>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>

      {error && <p className="text-sm text-red-600">{error}</p>}
    </div>
  )
}
