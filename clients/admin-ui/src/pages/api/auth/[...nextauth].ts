import NextAuth from 'next-auth';
import CredentialsProvider from 'next-auth/providers/credentials';

export default NextAuth({
  providers: [
    CredentialsProvider({
      name: 'Credentials',
      credentials: {
        email: {
          label: 'Email',
          type: 'text',
          placeholder: 'you@yourdomain.com',
        },
        password: { label: 'Password', type: 'password' },
      },
      async authorize(credentials) {
        // map email and password fields to client-level credentials temporarily
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_FIDESOPS_API!}/login`,
          {
            method: 'POST',
            body: JSON.stringify({
              username: credentials!.email,
              password: credentials!.password,
            }),
            headers: { 'Content-Type': 'application/json' },
          }
        );

        const user = await res.json();

        // If no error and we have user data, return it
        if (res.ok && user) {
          return {
            ...user,
            username: credentials!.email,
          };
        }

        // Return null if user data could not be retrieved
        return null;
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user?.access_token) {
        Object.assign(token, {
          token: user.access_token,
          username: user.username,
        });
      }

      return token;
    },
    async session({ session, token }) {
      Object.assign(session, {
        accessToken: token.token,
        username: token.username,
      });
      return session;
    },
  },
});
