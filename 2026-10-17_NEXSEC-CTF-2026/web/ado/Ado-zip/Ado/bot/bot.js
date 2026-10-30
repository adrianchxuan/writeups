const puppeteer = require('puppeteer')

const TARGET_URL = process.env.TARGET_URL || 'http://localhost:3333'
const ADMIN_USERNAME = process.env.ADMIN_USERNAME || 'admin'
const ADMIN_PASSWORD = process.env.ADMIN_BOT_PASSWORD // cred: admin password used to log the bot in
const INTERVAL_MS = Number(process.env.INTERVAL_MS || 15000)
const VISIT_TIMEOUT_MS = Number(process.env.VISIT_TIMEOUT_MS || 10000)

async function visitAsAdmin() {
  let browser
  try {
    browser = await puppeteer.launch({
      headless: 'new',
      userDataDir: '/tmp/puppeteer-profile',
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-crash-reporter',
        '--disable-breakpad',
        '--user-data-dir=/tmp/puppeteer-profile',
        '--crash-dumps-dir=/tmp/puppeteer-crashes',
      ],
    })

    const page = await browser.newPage()
    page.setDefaultTimeout(VISIT_TIMEOUT_MS)
    page.setDefaultNavigationTimeout(VISIT_TIMEOUT_MS)
    await page.goto(TARGET_URL, { waitUntil: 'domcontentloaded', timeout: VISIT_TIMEOUT_MS })

    const loginResp = await page.evaluate(
      async (url, username, password) => {
        const res = await fetch(url + '/api/v1/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify({ username, password }),
        })
        return { status: res.status, body: await res.text() }
      },
      TARGET_URL,
      ADMIN_USERNAME,
      ADMIN_PASSWORD
    )

    if (loginResp.status !== 200) {
      console.error(
        `[admin-bot] Login failed (status ${loginResp.status}): ${loginResp.body}`
      )
      return
    }
    await page.goto(`${TARGET_URL}/admin/comments`, {
      waitUntil: 'networkidle2',
      timeout: VISIT_TIMEOUT_MS,
    })
    await new Promise((resolve) => setTimeout(resolve, 2000))

    console.log(`[admin-bot] Visited /admin/comments at ${new Date().toISOString()}`)
  } catch (err) {
    console.error('[admin-bot] Error during visit:', err.message)
  } finally {
    if (browser) await browser.close()
  }
}

async function main() {
  console.log(`[admin-bot] Starting. Target: ${TARGET_URL}, interval: ${INTERVAL_MS}ms`)
  await visitAsAdmin()
  setInterval(visitAsAdmin, INTERVAL_MS)
}

main()