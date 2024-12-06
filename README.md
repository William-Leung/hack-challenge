## Route Explanation:
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
- If the user has not logged in, a `401` error is returned with the message "Invalid or missing token."

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
- If the user has not logged in, a `401` error is returned with the message "Invalid or missing token."

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
- If the user has not logged in, a `401` error is returned with the message "Invalid or missing token."

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
- If the user has not logged in, a `401` error is returned with the message "Invalid or missing token."

**Success Response:**
- A `200` status code is returned with a JSON object containing the deleted post.

---

## Database Explanation
### Relational Models

1. **User**
   - Represents users of the app.
   - Fields:
     - `id` (int, primary key)
     - `username` (str, unique, required)
     - `password_hash` (str, required)
     - `created_at` (datetime, defaults to current UTC time)
   - Relationship:
     - `posts` (one-to-many relationship with `Post`)

2. **Location**
   - Represents predefined locations identified by their names.
   - Fields:
     - `id` (int, primary key)
     - `name` (str, unique, required)
     - `latitude` (float, required)
     - `longitude` (float, required)
   - Relationship:
     - `posts` (one-to-many relationship with `Post`)

3. **Post**
   - Represents user-generated content tied to a specific location.
   - Fields:
     - `id` (int, primary key)
     - `user_id` (int, foreign key referencing `User.id`, required)
     - `location_name` (str, foreign key referencing `Location.name`, required)
     - `content` (text, required)
     - `likes` (int, defaults to 0)
     - `created_at` (datetime, defaults to current UTC time)
   - Relationships:
     - `user` (many-to-one relationship with `User`)
     - `location` (many-to-one relationship with `Location`)
   - Method:
     - `serialize`: Converts the post object to a dictionary for API responses.

The main design decision for this project was deciding how to represent locations. We chose to represent locations with names and convert longitude and latitude to a location name for a couple of reasons. Primarily, it's more elegant to move from the Slope chat to the Olin Library chat for example than be chatting with users in a radius around you. Having chats for each separate location made more sense. Thus, users' locations are converted into a location name based on the closest location. For the purpose of the app, we've hard coded a couple of locations: Tang Hall, Slope, Cocktail, etc. However, for the purpose of scalability, we imagine web scraping a list of famous Cornell buildings and their coordinates. 