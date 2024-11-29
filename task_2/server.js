const { ApolloServer } = require('apollo-server');
const typeDefs = require('./schema'); // Import type definitions
const resolvers = require('./resolver'); // Import resolvers
const jwt = require('jsonwebtoken');

const SECRET_KEY = "mysecretkey"; // Secret key for JWT verification

const server = new ApolloServer({
  typeDefs,
  resolvers,
  context: ({ req }) => {
    // Extract the token from the Authorization header
    const authHeader = req.headers.authorization || "";
    const token = authHeader.replace("Bearer ", "").trim();

    if (!token) {
      return { user: null }; // If no token is provided, user is not authenticated
    }

    try {
      // Verify the token and extract user information
      const user = jwt.verify(token, SECRET_KEY);
      return { user }; // Attach the user to the context
    } catch (err) {
      console.error("Authentication error:", err);
      return { user: null }; // Token is invalid or expired
    }
  },
});

server.listen().then(({ url }) => {
  console.log(`🚀 Server is running at ${url}`);
});
