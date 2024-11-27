const { gql } = require('apollo-server');

const typeDefs = gql`
    # Type for Books
    type Book {
        id: ID!
        title: String!
        author: String!
        publishedYear: Int!
    }

    # Type for Members
    type Member {
        id: ID!
        name: String!
        membershipType: String!
    }

    # Type for Users (used for login and role management)
    type User {
        id: ID!
        email: String!
        role: String!
    }

    # Root Query type
    type Query {
        # Fetch a single book by ID
        book(id: ID!): Book

        # Fetch all books
        books: [Book!]!

        # Fetch books published before 1950
        booksBefore1950: [Book!]!

        # Fetch a single member by ID
        member(id: ID!): Member

        # Fetch all members
        members: [Member!]!

        # Fetch secret data (requires authentication)
        secretData: String!
    }

    # Root Mutation type
    type Mutation {
        # Admin-only: Add a new book
        addBook(title: String!, author: String!, publishedYear: Int!): Book

        # Update a member's membership type
        updateMembership(id: ID!, membershipType: String!): Member

        # Login mutation to authenticate and return a JWT token
        login(email: String!, password: String!): String!
    }
`;

module.exports = typeDefs;
