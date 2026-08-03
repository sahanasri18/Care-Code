import { test } from 'node:test'
import assert from 'node:assert/strict'
import { authEpoch, bumpAuthEpoch, guardRefresh, StaleRefreshError } from '../src/api/authSession.js'

const deferred = () => {
  let resolve, reject
  const promise = new Promise((res, rej) => {
    resolve = res
    reject = rej
  })
  return { promise, resolve, reject }
}

test('guardRefresh passes when the session did not change', () => {
  const start = authEpoch()
  assert.doesNotThrow(() => guardRefresh(start))
})

test('a login during an in-flight refresh invalidates its result', async () => {
  const start = authEpoch()
  const pending = deferred()
  const applied = []
  const refreshResult = pending.promise.then((tokens) => {
    guardRefresh(start)
    applied.push(tokens)
  })

  tokenStoreSet() // user logs in again while the refresh is in flight
  pending.resolve('stale-tokens')

  await assert.rejects(refreshResult, StaleRefreshError)
  assert.deepEqual(applied, [], 'stale refresh must never apply its tokens')
})

test('a logout during an in-flight refresh invalidates its result', async () => {
  const start = authEpoch()
  const pending = deferred()
  const applied = []
  const refreshResult = pending.promise.then((tokens) => {
    guardRefresh(start)
    applied.push(tokens)
  })

  tokenStoreClear() // user logs out while the refresh is in flight
  pending.resolve('stale-tokens')

  await assert.rejects(refreshResult, StaleRefreshError)
  assert.deepEqual(applied, [])
})

test('consecutive login -> logout -> login cycles: only the current session refresh applies', async () => {
  const logins = []
  for (let i = 1; i <= 3; i += 1) {
    const start = authEpoch()
    const pending = deferred()
    const applied = []
    const refreshResult = pending.promise.then((tokens) => {
      guardRefresh(start)
      applied.push(tokens)
    })

    tokenStoreSet() // session for cycle i becomes active
    pending.resolve(`cycle-${i}-stale-tokens`)
    await assert.rejects(refreshResult, StaleRefreshError)
    assert.deepEqual(applied, [], `cycle ${i} stale refresh must not apply`)
    tokenStoreClear() // logout at the end of the cycle
    logins.push(`cycle-${i}-ok`)
  }

  tokenStoreSet() // fresh login for the final session
  const start = authEpoch()
  const pending = deferred()
  const applied = []
  const current = pending.promise.then((tokens) => {
    guardRefresh(start)
    applied.push(tokens)
  })

  pending.resolve('current-tokens')
  await current
  assert.deepEqual(applied, ['current-tokens'], 'current session refresh applies normally')
  assert.deepEqual(logins, ['cycle-1-ok', 'cycle-2-ok', 'cycle-3-ok'])
})

function tokenStoreSet() {
  bumpAuthEpoch()
}

function tokenStoreClear() {
  bumpAuthEpoch()
}
