# VoiceUp — backend

The Django REST API that VoiceUp's web and mobile apps both run on: accounts, complaints, backing, and comments, all behind one JWT-authenticated API.

## Why use it

- **One data source, two clients.** Web and mobile both hit the same API, so a complaint filed on a phone shows up correctly on the website and vice versa — no data to keep in sync by hand.
- **Hardened by default, not bolted on later.** Rate limiting on login/register, real password strength checks, and refresh-token blacklisting on logout are already in place, not left as "add before launch" TODOs.
- **Simple enough to run standalone.** It's a normal Django + DRF project behind Docker Compose — anyone building a third client (a bot, a dashboard, another app) has one straightforward REST API to call instead of reverse-engineering two frontends.
