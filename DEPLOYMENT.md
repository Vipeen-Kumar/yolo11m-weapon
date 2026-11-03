# Deployment Guide - YOLO11m Weapon Detection

This guide explains how to deploy the YOLO11m Weapon Detection application to Streamlit Community Cloud.

## Option 1: Deploy on Streamlit Community Cloud (Recommended)

Streamlit Community Cloud is the easiest and fastest way to deploy this app for free.

### Step 1: Prepare Your GitHub Repository ✅
- Repository is already set up at: https://github.com/Vipeen-Kumar/yolo11m-weapon
- All source code is committed
- Model weights (best.pt, 38.64 MB) are included
- Requirements.txt contains all dependencies

### Step 2: Create a Streamlit Account
1. Go to https://streamlit.io/cloud
2. Click "Sign up"
3. Sign in with your GitHub account (Vipeen-Kumar)
4. Authorize Streamlit to access your repositories

### Step 3: Deploy Your App
1. After signing in to Streamlit Cloud, click "New app"
2. Fill in the deployment details:
   - **Repository**: `Vipeen-Kumar/yolo11m-weapon`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
3. Click "Deploy"

### Step 4: Wait for Deployment
- First deployment takes 2-5 minutes
- Streamlit will:
  - Clone your repository
  - Install dependencies from requirements.txt
  - Download and cache the YOLO11m model
  - Start your application

### Step 5: Access Your App
Once deployed, your app will be live at:
```
https://yolo11m-weapon.streamlit.app
```
(The exact URL depends on your Streamlit Cloud workspace)

---

## Option 2: Deploy on Heroku (Alternative)

If Streamlit Cloud has resource limitations, you can use Heroku.

### Requirements
- Heroku account (free tier available)
- Heroku CLI installed
- Git configured

### Steps

1. **Create Heroku App**
   ```bash
   heroku login
   heroku create your-app-name
   ```

2. **Add Buildpacks**
   ```bash
   heroku buildpacks:add --index 1 heroku/python
   ```

3. **Create Procfile**
   ```
   web: streamlit run streamlit_app.py --server.port=$PORT --server.headless true
   ```

4. **Push to Heroku**
   ```bash
   git push heroku main
   ```

5. **View Logs**
   ```bash
   heroku logs --tail
   ```

---

## Option 3: Deploy on AWS (Advanced)

For production-grade deployment with custom infrastructure.

### Services Used
- **EC2**: Virtual server
- **S3**: Model storage (optional)
- **CloudWatch**: Monitoring

### Setup
1. Launch an EC2 instance (Ubuntu 20.04 LTS)
2. Install Python, dependencies, and Streamlit
3. Clone your GitHub repository
4. Run with: `streamlit run streamlit_app.py`
5. Use Nginx as reverse proxy

---

## Deployment Considerations

### Model Size
- **best.pt**: 38.64 MB
- **Total with dependencies**: ~200-300 MB
- **Fits within**: Streamlit Cloud (1GB limit) ✅

### Memory Requirements
- **Minimum**: 512 MB RAM
- **Recommended**: 1-2 GB RAM
- Streamlit Cloud provides: 1 GB ✅

### Dependencies
- PyTorch (large): ~400 MB
- OpenCV: ~100 MB
- Ultralytics YOLO: ~50 MB
- Other packages: ~50 MB

**Total**: ~600 MB (within Streamlit Cloud limits) ✅

### Performance Notes
- First model load takes 30-60 seconds
- Subsequent loads are cached
- Webcam access limited in cloud (requires user permission)
- Video processing depends on file size

---

## Troubleshooting

### App Won't Start
- Check logs: `streamlit run streamlit_app.py` locally first
- Verify all dependencies in requirements.txt
- Ensure Python version is 3.8+

### Model Loading Fails
- Check Internet connection (model may need to download)
- Verify best.pt is in repository
- Check available disk space (need ~100 MB free)

### Slow Performance
- First startup caches model (~1-2 min)
- Subsequent use is faster
- Video processing depends on CPU power
- Consider using smaller models or cloud GPU services

### Webcam Not Working in Cloud
- Webcam access is browser-dependent
- Deploy locally if webcam functionality is critical
- Use pre-recorded videos for testing in cloud

### Out of Memory
- Close other browser tabs
- Reduce video quality/resolution
- Use smaller model or cloud GPU tier

---

## Post-Deployment Verification

After deployment, verify all features work:

1. **✅ Load Model** - Click "Load Model" button
2. **✅ Image Detection** - Upload and test image
3. **✅ Video Detection** - Upload and test video (if possible)
4. **✅ Analytics** - Check model analytics dashboard
5. **✅ Download** - Download annotated results

---

## Monitoring & Maintenance

### Streamlit Cloud Dashboard
- Monitor app usage and resource consumption
- View logs and error messages
- Manage app settings and secrets

### Updating Your App
1. Push changes to GitHub main branch
2. Streamlit Cloud auto-detects changes
3. App redeploys automatically (~1-2 min)

### Sharing Your App
- Share public URL with anyone
- No login required for viewers
- Shareable link format: `https://yolo11m-weapon.streamlit.app`

---

## Performance Optimization

### For Cloud Deployment
```python
# Streamlit already uses these optimizations:
@st.cache_resource  # Cache model in memory
def load_model(model_name):
    return YOLO(model_name)
```

### Tips
- Use lighter confidence thresholds to reduce processing time
- Pre-process images before uploading
- Use webcam "Fast" or "Ultra Fast" modes
- Close unnecessary browser tabs

---

## Security Considerations

✅ **What's Secure**
- No API keys in code
- Model weights are public
- Input validation via Streamlit
- HTTPS by default on Streamlit Cloud

⚠️ **Recommendations for Production**
- Add authentication if needed
- Store sensitive configs in Streamlit Secrets
- Monitor for unusual usage patterns
- Rate limit if needed

---

## Need Help?

- **Streamlit Docs**: https://docs.streamlit.io/
- **Ultralytics YOLO**: https://docs.ultralytics.com/
- **GitHub Issues**: Report bugs on repository

---

**Last Updated**: November 2026
