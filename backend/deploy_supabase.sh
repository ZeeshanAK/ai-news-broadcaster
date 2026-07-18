#!/bin/bash

# Supabase deployment script for AI News Broadcaster

echo "Starting Supabase deployment..."

# Check if supabase CLI is installed
if ! command -v supabase &> /dev/null; then
    echo "Supabase CLI not found. Please install it first."
    echo "Visit: https://supabase.com/docs/guides/cli"
    exit 1
fi

# Check if we're in the correct directory
if [ ! -f "supabase/config.toml" ]; then
    echo "Supabase configuration not found. Please run 'supabase init' first."
    exit 1
fi

echo "Deploying database schema..."
supabase db push

echo "Deploying functions..."
supabase functions deploy

echo "Deployment complete!"
echo "Your Supabase project is now ready to use."