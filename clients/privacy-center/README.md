# fidesui-template

Shared NextJS template to build Fides UI applications

## Authentication

To enable stable authentication you must supply a `NEXTAUTH_SECRET` environment
variable. The best way to do this is by creating a `.env.local` file, which Next
will automatically pick up:

```bash
echo NEXTAUTH_SECRET=`openssl rand -base64 32` >> .env.local
```
