# Quick Deployment Reference

## 🚀 Deploy Backend to ngrok (5 minutes)

### Terminal 1: Start Backend
```bash
./start_backend.sh
```

### Terminal 2: Start ngrok
```bash
ngrok http 8000
```

**Copy the HTTPS URL** from ngrok output (e.g., `https://abc123.ngrok.io`)

### Terminal 3: Update CORS
```bash
./update_cors.sh https://abc123.ngrok.io
```

Then restart the backend (Ctrl+C in Terminal 1, then `./start_backend.sh` again)

---

## 🌐 Deploy Frontend to Vercel (3 minutes)

### Option 1: Vercel CLI
```bash
cd frontend
vercel
# Follow prompts, then:
vercel env add VITE_API_URL production
# Enter your ngrok URL: https://abc123.ngrok.io
vercel --prod
```

### Option 2: Vercel Dashboard
1. Go to https://vercel.com/new
2. Import your Git repo
3. Set Root Directory: `frontend`
4. Add env var: `VITE_API_URL` = `https://abc123.ngrok.io`
5. Deploy

---

## 📋 Checklist

- [ ] PostgreSQL running (`docker-compose up -d db`)
- [ ] Backend running (`./start_backend.sh`)
- [ ] ngrok tunnel active (`ngrok http 8000`)
- [ ] CORS updated with ngrok URL
- [ ] Frontend deployed to Vercel
- [ ] Vercel env var `VITE_API_URL` set
- [ ] CORS updated with Vercel URL
- [ ] Backend restarted after CORS update

---

## 🔗 URLs to Save

- **ngrok URL**: `https://________.ngrok.io`
- **Vercel URL**: `https://________.vercel.app`
- **ngrok Dashboard**: https://dashboard.ngrok.com
- **Vercel Dashboard**: https://vercel.com/dashboard

---

## 🛠️ Troubleshooting

### CORS Error
```bash
./update_cors.sh https://your-ngrok.ngrok.io https://your-app.vercel.app
# Restart backend
```

### ngrok URL Changed
```bash
# Get new URL from ngrok terminal
# Update Vercel env var
vercel env rm VITE_API_URL production
vercel env add VITE_API_URL production
# Enter new ngrok URL
vercel --prod
```

### Backend Not Responding
```bash
# Check if running
ps aux | grep uvicorn

# Check logs in backend terminal
# Restart if needed
```

---

## 📚 Full Documentation

See `NGROK_VERCEL_DEPLOYMENT.md` for detailed instructions.
