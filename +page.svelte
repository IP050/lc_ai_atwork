<script>
  let username = '';
  let password = '';
  let email = ''; // Only for registration

  async function register() {
    const response = await fetch('http://localhost:8000/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ username, email, password })
    });

    if (response.ok) {
      // Handle successful registration
      const data = await response.json();
      console.log('Registration successful', data);
    } else {
      // Handle errors
      const error = await response.json();
      console.error('Registration failed', error);
    }
  }

  async function login() {
    const response = await fetch('http://localhost:8000') 

  }

  </script> 
