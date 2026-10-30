import type { HttpContextContract } from '@ioc:Adonis/Core/HttpContext'
import store from 'App/Models/InMemoryStore'

export default class CommentsController {
  public async store({ request, response, session }: HttpContextContract) {
    const userId = session.get('userId')
    if (!userId) {
      return response.status(401).json({ error: 'Must be logged in to comment' })
    }

    const body = request.input('body', '')
    const postId = Number(request.input('postId', 1))

    if (!body) {
      return response.status(400).json({ error: 'body required' })
    }

    const comment = store.createComment({ userId, postId, body })

    return response.json({ message: 'Comment posted', id: comment.id })
  }

  public async publicIndex({ view, params }: HttpContextContract) {
    const postId = Number(params.postId)
    const comments = store
      .allComments()
      .filter((c) => c.postId === postId)
      .map((c) => ({ ...c, username: store.findUserById(c.userId)?.username }))

    return view.render('public/comments', { comments, postId })
  }

  public async adminIndex({ view, session, response }: HttpContextContract) {
    const role = session.get('role')
    if (role !== 'admin') {
      return response.status(403).json({ error: 'Admins only' })
    }

    const comments = store.allComments().map((c) => ({
      ...c,
      username: store.findUserById(c.userId)?.username,
    }))

    return view.render('admin/comments', { comments })
  }
}
