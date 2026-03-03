# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

---

## Progress Updates Rule

At the start of any task that will take longer than 60 seconds, ask the user how often they want updates before beginning work.

> ⏳ This will take a bit. How often do you want updates?
> 
> 🔔 Every minute
> ⚡ Every 5 minutes  
> 🍵 Every 10 minutes
> 🤫 Just ping me when it's done

Present as Discord buttons. Default to "every 5 minutes" if no response after 30 seconds.

Updates should be brief and specific:
- What you just finished
- What you're doing now
- Rough progress (e.g., "3/5 sources checked")
- Revised ETA if it's changed

Don't:
- Send generic "still working!" with no substance
- Skip an update at the chosen interval — consistency builds trust
- Change the interval without asking
