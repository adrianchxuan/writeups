import Route from '@ioc:Adonis/Core/Route'
import Application from '@ioc:Adonis/Core/Application'
import type { HttpContextContract } from '@ioc:Adonis/Core/HttpContext'
import { readFile } from 'node:fs/promises'

async function serveStaticFile(
  response: HttpContextContract['response'],
  filePath: string,
  extension: string
) {
  let contents: Buffer

  try {
    contents = await readFile(filePath)
  } catch (error) {
    if (
      typeof error === 'object' &&
      error !== null &&
      'code' in error &&
      error.code === 'ENOENT'
    ) {
      response.type('text')
      return response.status(404).send('File not found')
    }

    throw error
  }

  response.type(extension)
  response.header('cache-control', 'public, max-age=3600')
  return response.send(contents)
}

Route.get('/assets/Ado.jpg', async ({ response }) => {
  return serveStaticFile(response, Application.makePath('assets/Ado.jpg'), '.jpg')
})

Route.get('/assets/Ado-bg.svg', async ({ response }) => {
  return serveStaticFile(response, Application.makePath('assets/Ado-bg.svg'), '.svg')
})

Route.get('/css/ado-theme.css', async ({ response }) => {
  return serveStaticFile(response, Application.makePath('public/css/ado-theme.css'), '.css')
})

Route.get('/', async ({ view }) => {
  return view.render('welcome')
})

Route.get('/login', async ({ view }) => {
  return view.render('login')
})

Route.post('/api/v1/auth/login', 'AuthController.login')
Route.post('/api/v1/auth/logout', 'AuthController.logout')
Route.get('/api/v1/auth/me', 'AuthController.me')
Route.get('/api/v1/internal/accounts/:id', 'AccountsController.show')
Route.post('/api/v1/comments', 'CommentsController.store')
Route.get('/posts/:postId/comments', 'CommentsController.publicIndex')
Route.get('/admin', 'AdminUploadController.dashboard')
Route.get('/admin/comments', 'CommentsController.adminIndex')
Route.get('/admin/upload', 'AdminUploadController.dashboard')
Route.post('/admin/upload', 'AdminUploadController.upload')
Route.get('/admin/generate-report', 'AdminUploadController.generateReport')
