async function login(username, password) {
  // obtain CSRF
  const csrfRes = await fetch("http://localhost:8000/auth/csrf/", {
    credentials: "include",
  });
  const { csrfToken } = await csrfRes.json();

  // login
  const res = await fetch("http://localhost:8000/auth/login/", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify({ username, password }),
  });

  return res.json();
}
