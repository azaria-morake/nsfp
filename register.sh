#!/usr/bin/env bash
# Interactive register script with fixed endpoint

# 1) Fixed endpoint
BASE_URL="http://localhost:8000/api/register/"

# 2) Prompt for each field
read -p "Username: " USERNAME
read -sp "Password: " PASSWORD; echo
read -p "Team name: " TEAM_NAME
read -p "Location: " LOCATION
read -p "Email: " EMAIL

# 3) Build JSON payload (requires jq)
DATA=$(jq -n \
  --arg u "$USERNAME" \
  --arg p "$PASSWORD" \
  --arg t "$TEAM_NAME" \
  --arg l "$LOCATION" \
  --arg e "$EMAIL" \
  '{username: $u, password: $p, team_name: $t, location: $l, email: $e}')

# 4) Send the POST request
echo -e "\nSending request to $BASE_URL"
curl -i -X POST "$BASE_URL" \
     -H "Content-Type: application/json" \
     -d "$DATA"
