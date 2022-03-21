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
        const data = new URLSearchParams();
        data.append('client_id', credentials!.email);
        data.append('client_secret', credentials!.password);
        const res = await fetch(process.env.NEXT_PUBLIC_AUTH_ENDPOINT!, {
          method: 'POST',
          body: data,
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });
        const user = await res.json();

        // If no error and we have user data, return it
        if (res.ok && user) {
          return user;
        }

        // Return null if user data could not be retrieved
        return null;
      },
    }),
  ],
});
