# Quartz Trigger Setup for Obsidian Repo

This file explains how to complete the setup for automatic Quartz deployment when content changes in this Obsidian repository.

## What's Already Set Up

✅ **Trigger workflow created**: `.github/workflows/trigger-quartz-sync.yml`
- Watches for changes in Calendar, Notes, Vault.md, and index.md
- Automatically triggers Quartz sync when content changes

## What You Need to Do

### 1. Generate Personal Access Token

1. Go to GitHub → `Settings` → `Developer settings` → `Personal access tokens` → `Tokens (classic)`
2. Click `Generate new token (classic)`
3. Give it a name like "Quartz Sync"
4. Select scope: `repo` (full control of private repositories)
5. Copy the token (you'll need it for the next step)

### 2. Add Repository Secrets

In this Obsidian repository:
1. Go to `Settings` → `Secrets and variables` → `Actions`
2. Click `New repository secret`
3. Add these two secrets:

   **Secret 1:**
   - Name: `QUARTZ_REPO_TOKEN`
   - Value: [Your personal access token from step 1]

   **Secret 2:**
   - Name: `QUARTZ_REPO`
   - Value: `Rupali59/quartz`

### 3. Commit and Push

```bash
git add .github/workflows/trigger-quartz-sync.yml
git add QUARTZ_TRIGGER_SETUP.md
git commit -m "Add GitHub Actions trigger for Quartz sync"
git push origin main
```

## How It Works

1. **You make changes** to Calendar, Notes, Vault.md, or index.md
2. **You commit and push** to this Obsidian repo
3. **Trigger workflow runs** automatically
4. **Sends notification** to your Quartz repo
5. **Quartz syncs content** and deploys automatically

## Testing

After setup:
1. Make a small change to any note
2. Commit and push
3. Check your Quartz repo Actions tab - you should see the sync workflow running!

## Troubleshooting

- **Workflow not running**: Check if GitHub Actions are enabled for this repo
- **Permission errors**: Verify the personal access token has `repo` scope
- **No trigger**: Make sure you're pushing to the `main` branch
- **Wrong paths**: The workflow only triggers for changes in Calendar/, Notes/, Vault.md, or index.md

## Security Notes

- The personal access token only needs `repo` scope
- It's stored securely as a repository secret
- The workflow only sends notifications, doesn't access your content directly
