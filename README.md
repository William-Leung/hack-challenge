Route Explanation:


### 1. `POST /register/`

**Required Fields:**
- `username` (string)
- `password` (string)

**Description:**
This route allows users to create a new account by providing a unique username and a password. 

**Error Handling:**
- If either `username` or `password` is missing, a `400` error is returned with the message "Missing username or password."
- If the username already exists, a `400` error is returned with the message "User already exists."

**Success Response:**
- A `201` status code is returned with the message "User registered successfully."

---

### 2. `POST /login/`

**Required Fields:**
- `username` (string)
- `password` (string)

**Description:**
This route allows existing users to log in by providing their username and password. Upon successful login, an access token is generated and returned.

**Error Handling:**
- If either `username` or `password` is missing, a `400` error is returned with the message "Missing username or password."
- If the credentials are invalid (e.g., the username does not exist or the password is incorrect), a `401` error is returned with the message "Invalid credentials. Please register as a new user."

**Success Response:**
- A `200` status code is returned with a JSON object containing the access token.

---

### 3. `GET /posts/`

**Required Fields:**
- `latitude` (float)
- `longitude` (float)

**Description:**
This route retrieves all posts at the nearest location to the provided latitude and longitude.

**Error Handling:**
- If either `latitude` or `longitude` is missing, a `400` error is returned with the message "Latitude and longitude are required."
- If no nearby location is found, a `404` error is returned with the message "No nearby locations found."

**Success Response:**
- A `200` status code is returned with a JSON object containing the retrieved posts.

---

### 4. `POST /posts/`

**Required Fields:**
- `latitude` (float)
- `longitude` (float)
- `content` (string)
- `user_id` (int)

**Description:**
This route allows a user to create a new post by providing the content, latitude, longitude, and user ID.

**Error Handling:**
- If any of `content`, `latitude`, `longitude`, or `user_id` are missing, a `400` error is returned with the message "Content, latitude, and longitude are required."
- If no nearby location is found based on the provided latitude and longitude, a `404` error is returned with the message "No nearby location found."

**Success Response:**
- A `201` status code is returned with a JSON object containing the new post.

---

### 5. `POST /posts/<int:post_id>/like/`

**Required Fields:**
- None

**Description:**
This route allows users to like a post.

**Error Handling:**
- If the specified post does not exist, a `404` error is returned with the message "Post not found."

**Success Response:**
- A `200` status code is returned with a JSON object containing the liked post.

---

### 6. `DELETE /posts/<int:post_id>/`

**Required Fields:**
- None

**Description:**
This route allows users to delete a post.

**Error Handling:**
- If the specified post ID does not exist, a `404` error is returned with the message "Post not found."

**Success Response:**
- A `200` status code is returned with a JSON object containing the deleted post.