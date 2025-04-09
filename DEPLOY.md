# Deployment Instructions for Patient Data Automation API

This guide outlines how to deploy the Patient Data Automation API to Render.com, a cloud service that makes deployment simple.

## Prerequisites

1. Create a [Render.com](https://render.com/) account if you don't have one already
2. Make sure your project is in a Git repository (GitHub, GitLab, etc.)

## Steps to Deploy

### 1. Prepare Your Repository

Make sure your repository has:
- `requirements.txt` (with all dependencies)
- `Procfile` (with the command to run the app)
- Proper directory structure

### 2. Create a New Web Service on Render

1. Log in to your Render dashboard
2. Click "New" in the top right corner
3. Select "Web Service" from the dropdown

### 3. Connect Your Repository

1. Choose the repository where your code is stored
2. If your repo is not listed, you may need to grant Render access to your GitHub/GitLab account

### 4. Configure Your Web Service

Use these settings for your web service:
- **Name**: patient-data-automation (or your preferred name)
- **Runtime**: Python
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn --chdir src api_server:app`
- **Instance Type**: Free (for testing) or Basic (for production)
- **Environment Variables**:
  - `FLASK_ENV`: production
  - `PORT`: 8000

### 5. Advanced Settings (Optional)

You may want to set up:
- **Auto-Deploy**: Enabled by default, every push to your main branch will trigger a new deployment
- **Health Check Path**: `/health` (this is already implemented in the API)

### 6. Deploy

Click "Create Web Service" to deploy your application. The initial build may take a few minutes.

### 7. Access Your API

Once deployed, your API will be available at the URL provided by Render (usually `https://your-service-name.onrender.com`).

### 8. Troubleshooting

If you encounter any issues:
1. Check the Render logs for error messages
2. Verify all dependencies are in requirements.txt
3. Check if your application is properly binding to the PORT environment variable
4. Verify all necessary directories are created by the application on startup

### 9. Production Considerations

For a production environment, consider:
- Adding authentication to protect your API endpoints
- Configuring SSL (handled automatically by Render)
- Setting up a database for persistent storage instead of relying on file system
- Adding rate limiting to prevent abuse
