import { cpSync, existsSync, mkdirSync, rmSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = join(dirname(fileURLToPath(import.meta.url)), '..')
const dist = join(root, 'frontend', 'dist')
const netlifyDrop = join(root, 'netlify-drop')

if (!existsSync(dist)) {
  console.error('Build the frontend first: npm run build:frontend')
  process.exit(1)
}

rmSync(netlifyDrop, { recursive: true, force: true })
mkdirSync(netlifyDrop, { recursive: true })
cpSync(dist, netlifyDrop, { recursive: true })

console.log('')
console.log('Ready to deploy: netlify-drop/')
console.log('')
console.log('1. Edit netlify-drop/config.js with your Vercel API URL')
console.log('2. Drag netlify-drop/ onto https://app.netlify.com/drop')
console.log('')
