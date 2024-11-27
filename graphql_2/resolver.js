const jwt = require("jsonwebtoken");

// Mock user database
const users = [
  { id: 1, email: "alice@example.com", password: "password123", role: "USER" },
  { id: 2, email: "admin@example.com", password: "admin123", role: "ADMIN" },
];

// Secret key for JWT
const SECRET_KEY = "mysecretkey";

// In-memory data for Books and Members
const Books = [
  { id: 1, title: "To Kill a Mockingbird", author: "Harper Lee", publishedYear: 1960 },
  { id: 2, title: "1984", author: "George Orwell", publishedYear: 1949 },
  { id: 3, title: "The Great Gatsby", author: "F. Scott Fitzgerald", publishedYear: 1925 },
];

const Members = [
  { id: 1, name: "Alice", email: "alice@example.com", membershipType: "Premium", role: "USER" },
  { id: 2, name: "Bob", email: "bob@example.com", membershipType: "Basic", role: "ADMIN" },
];

const resolvers = {
  Query: {
    book: (_, { id }) => Books.find((book) => book.id === Number(id)),
    books: () => Books,
    booksBefore1950: () => Books.filter((book) => book.publishedYear < 1950),
    member: (_, { id }) => Members.find((member) => member.id === Number(id)),
    members: () => Members,
  },

  Mutation: {
    // Add a new book (Admin only)
    addBook: (_, { title, author, publishedYear }, { token }) => {
      // Check if the user is authenticated
      if (!token) {
        throw new Error("Authentication required: Token not found");
      }

      try {
        const user = jwt.verify(token, SECRET_KEY);

        // Allow only admins to add a new book
        if (user.role !== "ADMIN") {
          throw new Error("Authorization failed: Only admins can add new books");
        }

        const newBook = {
          id: Books.length + 1,
          title,
          author,
          publishedYear,
        };

        Books.push(newBook);
        return newBook;
      } catch (err) {
        if (err.name === "TokenExpiredError") {
          throw new Error("Authentication failed: Token has expired");
        } else if (err.name === "JsonWebTokenError") {
          throw new Error("Authentication failed: Invalid token");
        }
        throw new Error(err.message || "Authentication failed: Unknown error");
      }
    },

    // Update membership (Any user can update their membership)
    updateMembership: (_, { id, membershipType }) => {
      const member = Members.find((member) => member.id === Number(id));
      if (!member) {
        throw new Error("Member not found!");
      }
      member.membershipType = membershipType;
      return member;
    },

    // Login mutation to authenticate the user and return a JWT token
    login: (_, { email, password }) => {
      const user = users.find((user) => user.email === email && user.password === password);
      if (!user) {
        throw new Error("Invalid credentials");
      }

      const token = jwt.sign({ id: user.id, role: user.role }, SECRET_KEY, {
        expiresIn: "1h",
      });

      return token;
    },
  },
};

module.exports = resolvers;
