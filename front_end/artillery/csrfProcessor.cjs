const axios = require('axios');

let globalCsrfToken = null;

async function fetchCsrfToken(context, events, done) {
  try {
    // Fetch CSRF token from your Django endpoint
    const response = await axios.get('http://localhost/api/user/get_csrf/');
    const csrfToken = response.data; // Assuming the response is plain text

    console.log('Fetched CSRF token:', csrfToken)

    // Your existing logic to fetch the CSRF token
    globalCsrfToken = 'fetched_token_value'; // Assume this is your fetched token

    if (!globalCsrfToken) {
      throw new Error('CSRF token not found');
    }

    // Attempt to use global variable as a fallback
    if (!context.vars) context.vars = {};
    context.vars.csrfToken = globalCsrfToken;

    done();
  } catch (error) {
    console.error('Failed to fetch CSRF token:', error);
    done(error);
  }
}

module.exports = { fetchCsrfToken };
