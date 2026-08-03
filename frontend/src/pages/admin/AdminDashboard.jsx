import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { client, apiError } from '../../api/client'
import { PageLoader, StatCard } from '../../components/ui'

export default function AdminDashboard() {
  const [stats, setStats] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    client
      .get('/api/v1/admin/stats')
      .then((res) => setStats(res.data))
      .catch((err) => setError(apiError(err)))
  }, [])

  if (!stats) return error ? <p className="text-red-600">{error}</p> : <PageLoader />

  return (
    <div className="space-y-6">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <div>
          <h1 className="text-2xl font-extrabold text-slate-900">Admin overview</h1>
          <p className="text-sm text-slate-500">Platform-wide metrics.</p>
        </div>
        <div className="flex gap-2">
          <Link to="/admin/hospitals" className="btn-outline !py-2 text-xs">
            Manage hospitals
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <StatCard label="Total users" value={stats.total_users} sub={`${stats.active_users} active`} />
        <StatCard label="Medical profiles" value={stats.total_profiles} />
        <StatCard label="Total scans" value={stats.total_scans} sub={`${stats.scans_last_30_days} in 30 days`} />
        <StatCard label="Hospitals" value={stats.total_hospitals} sub={`${stats.signups_last_30_days} new users (30d)`} />
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <section className="card">
          <h2 className="mb-4 font-bold text-slate-900">Signups — last 30 days</h2>
          {stats.signups_per_day.length === 0 ? (
            <p className="text-sm text-slate-500">No signups recorded.</p>
          ) : (
            <div className="flex h-32 items-end gap-1">
              {stats.signups_per_day.map((d) => (
                <div key={d.date} className="flex flex-1 flex-col items-center gap-1">
                  <span className="text-[10px] font-semibold text-slate-500">{d.count}</span>
                  <div
                    className="w-full rounded-t bg-primary"
                    style={{ height: `${Math.min(100, d.count * 12)}%`, minHeight: 4 }}
                    title={`${d.date}: ${d.count}`}
                  />
                </div>
              ))}
            </div>
          )}
        </section>

        <section className="card border-dashed">
          <h2 className="mb-2 font-bold text-slate-900">Privacy first</h2>
          <p className="text-sm leading-relaxed text-slate-600">
            CareCode is designed so that personal accounts and emergency medical profiles stay entirely under each
            user's control. Administrators cannot view, edit, delete, or access any user's account or medical data —
            admins only manage application resources like hospitals and see aggregate platform analytics.
          </p>
        </section>
      </div>
    </div>
  )
}
