import { beforeEach, expect, test, vi } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import App from './App'

beforeEach(() => {
  cleanup()
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

test('shows a sign-in form for an unauthenticated visitor', () => {
  localStorage.clear()
  render(<App />)
  expect(screen.getByRole('button', { name: 'Sign in' })).toBeTruthy()
})

test('shows a customer search field for filtering inventory', () => {
  localStorage.clear()
  const payload = btoa(JSON.stringify({ role: 'user' }))
  localStorage.setItem('accessToken', `header.${payload}.signature`)
  render(<App />)
  expect(screen.getByPlaceholderText('Search make, model, or category')).toBeTruthy()
})

test('purchases an in-stock vehicle and updates its quantity', async () => {
  localStorage.clear()
  const payload = btoa(JSON.stringify({ role: 'user' }))
  localStorage.setItem('accessToken', `header.${payload}.signature`)
  const fetchMock = vi.fn()
    .mockResolvedValueOnce({ ok: true, json: async () => [{ id: 'vehicle-1', make: 'Toyota', model: 'Camry', category: 'Sedan', price: 28000, quantity: 3 }] })
    .mockResolvedValueOnce({ ok: true, json: async () => ({ id: 'vehicle-1', make: 'Toyota', model: 'Camry', category: 'Sedan', price: 28000, quantity: 2 }) })
  vi.stubGlobal('fetch', fetchMock)

  render(<App />)
  fireEvent.click(await screen.findByRole('button', { name: 'Purchase vehicle' }))

  expect(await screen.findByText('2 in stock')).toBeTruthy()
  expect(fetchMock.mock.calls[1][0]).toContain('/api/vehicles/vehicle-1/purchase')
  expect(fetchMock.mock.calls[1][1].method).toBe('POST')
})
