# backend (Django REST API)

Serves the citizen complaints data and auth to both the web and mobile clients.

| Function | Why it's needed |
|---|---|
| JWT login / register / refresh / logout | Web and mobile share one stateless auth system — no server-side sessions to keep in sync across two clients. |
| Refresh-token blacklisting on logout | Without it, a stolen refresh token stays valid for its full lifetime even after the user logs out. |
| Rate limiting (login, register, global) | Stops credential-stuffing and registration spam without adding a separate service. |
| Real password strength validation | The setting existed but was never enforced — users could set trivial passwords despite the config. |
| Complaints CRUD | The core record: what happened, who's responsible, where, current status. |
| Categories / Companies / Regions endpoints | One shared source of truth for filter/picker options, instead of hardcoding the same lists twice (web + mobile). |
| Backing (`/complaints/{id}/back/`) | Lets other affected citizens say "this happened to me too" — the count is what turns one complaint into visible collective pressure. |
| Comments | Public corroboration and updates on a case, without needing a separate messaging system. |
| Status history | Keeps a record of how a complaint moved through received → in progress → resolved, so outcomes aren't just overwritten and lost. |
| Photo upload with size cap | Citizens need to attach evidence (bills, meter photos); the cap stops the media volume from growing unbounded. |
| `/api/users/me/` | Lets a logged-in client fetch its own profile without re-sending credentials on every screen. |
