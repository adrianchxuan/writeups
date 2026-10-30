import type { HttpContextContract } from '@ioc:Adonis/Core/HttpContext'
import store from 'App/Models/InMemoryStore'

export default class AuthController {
  public async login({ request, response, session }: HttpContextContract) {
    const username = request.input('username', '')
    const password = request.input('password', '')

    const user = store.findUserByUsername(username)

    if (!user || user.password !== password) {
      return response.status(401).json({
        error: 'Invalid credentials'
    })}

    session.put('userId', user.id)
    session.put('role', user.role)

    return response.json({ message: 'Logged in', username: user.username, role: user.role })
  }

  public async logout({ session, response }: HttpContextContract) {
    session.clear()
    return response.json({ message: 'Logged out' })
  }

  public async me({ session, response }: HttpContextContract) {
    const userId = session.get('userId')
    if (!userId) return response.status(401).json({ error: 'Not logged in' })
    const user = store.findUserById(userId)
    return response.json({ id: user?.id, username: user?.username, role: user?.role })
  }
}
