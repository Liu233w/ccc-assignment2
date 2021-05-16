const config = require('./config')
const fs = require('fs/promises')
const axios = require('axios').default

const VIEW_NAME = 'suburb_category'
const BASE_URL = withoutTrailingSlash(config.backendUrl)

async function main() {
  const view = await fs.readFile('./dest/view.js')

  await axios.put(`${BASE_URL}/api/analysis/${VIEW_NAME}`, {
    map: view.toString(),
    reduce: '_count',
  }, {
    maxContentLength: Infinity,
    maxBodyLength: Infinity,
  })
    .then(_ => console.log('success'))
    .catch(e => console.log(e.response ? e.response.data : e.message))

}

/**
 *  
 * @param {string} str 
 * @returns 
 */
function withoutTrailingSlash(str) {
  if (str[str.length - 1] === '/') {
    return str.substr(0, str.length - 1)
  } else {
    return str
  }
}

main()