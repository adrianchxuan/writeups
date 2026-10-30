import type { HttpContextContract } from '@ioc:Adonis/Core/HttpContext'
import store from 'App/Models/InMemoryStore'

export default class AccountsController {
  public async show({ params, response }: HttpContextContract) {
    const id = Number(params.id)
    const user = store.findUserById(id)

    if (!user) {
      return response.status(404).json({ error: 'Account not found' })
    }

    if (user.username !== 'Hana' && user.username !== 'Rimi') {
      return response.status(404).json({ error: 'Account not found' })
    }

    return response.json({
      id: user.id,
      username: user.username,
      email: user.email,
      recoveryToken: user.recoveryToken,
      password: user.password,
    })
  }
}
