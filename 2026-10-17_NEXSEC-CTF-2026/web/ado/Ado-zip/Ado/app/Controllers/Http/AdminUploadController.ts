import type { HttpContextContract } from '@ioc:Adonis/Core/HttpContext'
import Application from '@ioc:Adonis/Core/Application'
import { join } from 'node:path'

const STORAGE_ROOT = Application.makePath('storage')
const UPLOADS_DIR = join(STORAGE_ROOT, 'uploads')
const REPORTS_DIR = join(STORAGE_ROOT, 'reports')

export default class AdminUploadController {
  public async dashboard({ view, response, session }: HttpContextContract) {
    if (session.get('role') !== 'admin') {
      return response.status(403).json({ error: 'Admins only' })
    }

    return view.render('admin/dashboard')
  }

  public async upload({ request, response, session }: HttpContextContract) {
    const role = session.get('role')
    if (role !== 'admin') {
      return response.status(403).json({ error: 'Admins only' })
    }

    const file = request.file('attachment')
    if (!file) {
      return response.status(400).json({ error: 'attachment file required' })
    }

    await file.move(UPLOADS_DIR)

    return response.json({
      message: 'Attachment uploaded',
      storedAs: file.fileName,
    })
  }

  public async generateReport({ response, session }: HttpContextContract) {
    const role = session.get('role')
    if (role !== 'admin') {
      return response.status(403).json({ error: 'Admins only' })
    }

    try {
      const fs = require('fs')
      const vm = require('vm')
      const templatePath = join(REPORTS_DIR, 'template.js')

      const code = fs.readFileSync(templatePath, 'utf8')

      const sandbox: { module: { exports: any } } = { module: { exports: {} } }
      vm.createContext(sandbox)
      vm.runInContext(code, sandbox, { filename: templatePath })

      const template = sandbox.module.exports
      const result = typeof template.generate === 'function' ? template.generate() : null

      return response.json({ message: 'Report generated', result })
    } catch (error) {
      return response.status(500).json({ error: 'Report generation failed', detail: String(error) })
    }
  }
}