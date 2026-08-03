export class StaleRefreshError extends Error {
  constructor() {
    super('session changed during refresh')
    this.name = 'StaleRefreshError'
  }
}

let epoch = 0

export function bumpAuthEpoch() {
  epoch += 1
}

export function authEpoch() {
  return epoch
}

export function guardRefresh(epochAtStart) {
  if (epochAtStart !== epoch) throw new StaleRefreshError()
}
