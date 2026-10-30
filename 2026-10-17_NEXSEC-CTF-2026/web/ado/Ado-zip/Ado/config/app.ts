import Env from '@ioc:Adonis/Core/Env'
import Application from '@ioc:Adonis/Core/Application'
import { ServerConfig } from '@ioc:Adonis/Core/Server'

export const appKey: string = Env.get('APP_KEY')

export const http: ServerConfig = {
  allowMethodSpoofing: false,
  subdomainOffset: 2,
  generateRequestId: false,
  trustProxy: () => true,
  etag: false,
  jsonpCallbackName: 'callback',
  cookie: {
    domain: '',
    path: '/',
    maxAge: '2h',
    httpOnly: false,
    secure: false,
    sameSite: false,
  },
}

export const logger = {
  name: Env.get('APP_NAME', 'Ado'),
  enabled: true,
  level: Env.get('LOG_LEVEL', 'info'),
  prettyPrint: Application.inDev,
}

export const profiler = {
  enabled: true,
  blacklist: [],
  whitelist: [],
}
