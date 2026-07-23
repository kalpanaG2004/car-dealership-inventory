import { beforeEach, expect, test, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import App from './App'

beforeEach(() => {
  localStorage.clear()
  const payload = btoa(JSON.stringify({ role: 'admin' }))
  localStorage.setItem('accessToken', `header.${payload}.signature`)
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue({
      ok: true,
      json: async () => [
        { id: 'vehicle-1', make: 'Toyota', model: 'Camry', category: 'Sedan', price: 28000, quantity: 3 },
      ],
    }),
  )
})

test('shows restock and delete controls for an administrator', async () => {
  render(<App />)
  expect(await screen.findByRole('button', { name: 'Restock' })).toBeTruthy()
  expect(screen.getByRole('button', { name: 'Delete vehicle' })).toBeTruthy()
})

test('shows an edit action for an administrator', async () => {
  render(<App />)
  expect(await screen.findByRole('button', { name: 'Edit vehicle' })).toBeTruthy()
})
