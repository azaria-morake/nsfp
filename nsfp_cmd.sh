#!/usr/bin/env bash
# Master Control Script for Team Management with Token Prompting

# ============================================================
# Team Management CLI Tool
# This script allows you to:
# 1. Register a new team (creates a user account)
# 2. Add staff to a team
# 3. Refresh access tokens for a team
# 4. Add squad members
# 5. Login to get new access + refresh tokens
# 6. Change Access Token manually
# 7. Post Team Need
# 8. Upload Photo
# 9. Add Video Link
# 10. Delete Photo
# ============================================================
# Requirements:
# - jq (for JSON parsing)
# - curl (for API requests)
# - A running API server at http://localhost:8000
# ============================================================

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "jq could not be found. Please install jq to use this script."
    exit 1
fi
# Check if curl is installed
if ! command -v curl &> /dev/null; then
    echo "curl could not be found. Please install curl to use this script."
    exit 1
fi

# Token storage configuration
TOKEN_DIR=".tokens"
if [ ! -d "$TOKEN_DIR" ]; then
    mkdir -p "$TOKEN_DIR"
fi

# Base URL for API requests
BASE_URL="http://localhost:8000"

# Colors for feedback
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[1;34m'
NC='\033[0m' # No Color

# Helper: Load token from token directory
get_token() {
    local TEAM_FILE="${TOKEN_DIR}/${1}_token"
    if [ -f "$TEAM_FILE" ]; then
        cat "$TEAM_FILE"
    else
        echo "null"
    fi
}

# Helper: Save token to token directory
save_token() {
    local TEAM_FILE="${TOKEN_DIR}/${1}_token"
    echo "$2" > "$TEAM_FILE"
}

# Helper: Prompt for a token (used when team name is known)
prompt_for_token() {
    while true; do
        read -p "Enter Team Name (or type 'cancel' to return to main menu): " TEAM_NAME
        if [[ "$TEAM_NAME" == "cancel" ]]; then
            echo -e "${RED}↩️  Cancelled. Returning to main menu.${NC}"
            return 1
        fi

        ACTION_TOKEN=$(get_token "$TEAM_NAME")
        if [ "$ACTION_TOKEN" == "null" ] || [ -z "$ACTION_TOKEN" ]; then
            echo -e "${RED}❌ No token found for '$TEAM_NAME'. Please try again.${NC}"
        else
            return 0
        fi
    done
}

# ========== Add Team ==========
add_team() {
    echo -e "${BLUE}\nRegister a new team (type 'cancel' at any point to go back)\n${NC}"

    read -p "Username: " USERNAME
    [[ "$USERNAME" == "cancel" ]] && echo -e "${RED}↩️  Cancelled.${NC}" && return

    read -p "Password: " PASSWORD
    [[ "$PASSWORD" == "cancel" ]] && echo -e "${RED}↩️  Cancelled.${NC}" && return

    read -p "Email: " EMAIL
    [[ "$EMAIL" == "cancel" ]] && echo -e "${RED}↩️  Cancelled.${NC}" && return

    read -p "Team Name: " TEAM_NAME
    [[ "$TEAM_NAME" == "cancel" ]] && echo -e "${RED}↩️  Cancelled.${NC}" && return

    read -p "Location: " LOCATION
    [[ "$LOCATION" == "cancel" ]] && echo -e "${RED}↩️  Cancelled.${NC}" && return

    DATA=$(jq -n \
      --arg u "$USERNAME" \
      --arg p "$PASSWORD" \
      --arg e "$EMAIL" \
      --arg t "$TEAM_NAME" \
      --arg l "$LOCATION" \
      '{username: $u, password: $p, email: $e, team_name: $t, location: $l}')

    echo -e "\n${BLUE}Registering team...${NC}"
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/register/" \
         -H "Content-Type: application/json" \
         -d "$DATA")

    HTTP_BODY=$(echo "$RESPONSE" | head -n -1)
    HTTP_CODE=$(echo "$RESPONSE" | tail -n 1)

    echo -e "${BLUE}Server response:${NC}"
    echo "$HTTP_BODY" | jq . 2>/dev/null || echo "$HTTP_BODY"
}

# ========== Add Staff Member ==========
add_staff() {
    if ! prompt_for_token; then return; fi

    read -p "Username (or type 'cancel' to return): " USERNAME
    [[ "$USERNAME" == "cancel" ]] && echo -e "${RED}↩️  Cancelled.${NC}" && return

    read -p "Full Name (or type 'cancel' to return): " FULL_NAME
    [[ "$FULL_NAME" == "cancel" ]] && echo -e "${RED}↩️  Cancelled.${NC}" && return

    read -p "Role (or type 'cancel' to return): " ROLE
    [[ "$ROLE" == "cancel" ]] && echo -e "${RED}↩️  Cancelled.${NC}" && return

    DATA=$(jq -n \
      --arg u "$USERNAME" \
      --arg f "$FULL_NAME" \
      --arg r "$ROLE" \
      '{username: $u, full_name: $f, role: $r}')

    echo -e "\n${BLUE}Adding staff member...${NC}"
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/staff/" \
         -H "Authorization: Bearer $ACTION_TOKEN" \
         -H "Content-Type: application/json" \
         -d "$DATA")

    HTTP_BODY=$(echo "$RESPONSE" | head -n -1)

    echo -e "${BLUE}Server response:${NC}"
    echo "$HTTP_BODY" | jq . 2>/dev/null || echo "$HTTP_BODY"
}

# ========== Refresh Token ==========
refresh_token() {
    read -p "Team Name (or type 'cancel' to return): " TEAM_NAME
    [[ "$TEAM_NAME" == "cancel" ]] && echo -e "${RED}↩️  Cancelled.${NC}" && return

    read -p "Refresh Token: " REFRESH

    echo -e "\n${BLUE}Refreshing token...${NC}"
    DATA=$(jq -n --arg r "$REFRESH" '{refresh: $r}')
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/token/refresh/" \
         -H "Content-Type: application/json" \
         -d "$DATA")

    HTTP_BODY=$(echo "$RESPONSE" | head -n -1)
    HTTP_CODE=$(echo "$RESPONSE" | tail -n 1)

    echo -e "${BLUE}Full response:${NC}"
    echo "$HTTP_BODY" | jq . 2>/dev/null || echo "$HTTP_BODY"

    ACCESS=$(echo "$HTTP_BODY" | jq -r '.access // empty')

    if [[ -n "$ACCESS" ]]; then
        save_token "$TEAM_NAME" "$ACCESS"
        echo -e "${GREEN}✅ Token refreshed and saved for $TEAM_NAME${NC}"
    else
        echo -e "${RED}❌ Failed to refresh token.${NC}"
    fi
}

# ========== Add Squad Member ==========
add_squad() {
    if ! prompt_for_token; then return; fi

    read -p "Username (or type 'cancel' to return): " USERNAME
    [[ "$USERNAME" == "cancel" ]] && echo -e "${RED}↩️  Cancelled.${NC}" && return

    read -p "Full Name (or type 'cancel' to return): " FULL_NAME
    [[ "$FULL_NAME" == "cancel" ]] && echo -e "${RED}↩️  Cancelled.${NC}" && return

    read -p "Date of Birth (YYYY-MM-DD): " DOB
    [[ "$DOB" == "cancel" ]] && echo -e "${RED}↩️  Cancelled.${NC}" && return

    read -p "Citizenship: " CITIZENSHIP
    [[ "$CITIZENSHIP" == "cancel" ]] && echo -e "${RED}↩️  Cancelled.${NC}" && return

    read -p "Strong Foot (left/right): " STRONG_FOOT
    [[ "$STRONG_FOOT" == "cancel" ]] && echo -e "${RED}↩️  Cancelled.${NC}" && return

    read -p "Jersey Number: " JERSEY_NUMBER
    [[ "$JERSEY_NUMBER" == "cancel" ]] && echo -e "${RED}↩️  Cancelled.${NC}" && return

    read -p "Position (or type 'cancel' to return): " POSITION
    [[ "$POSITION" == "cancel" ]] && echo -e "${RED}↩️  Cancelled.${NC}" && return

    DATA=$(jq -n \
      --arg u "$USERNAME" \
      --arg f "$FULL_NAME" \
      --arg d "$DOB" \
      --arg c "$CITIZENSHIP" \
      --arg s "$STRONG_FOOT" \
      --arg j "$JERSEY_NUMBER" \
      --arg p "$POSITION" \
      '{username: $u, full_name: $f, dob: $d, citizenship: $c, strong_foot: $s, jersey_number: $j, position: $p}')

    echo -e "\n${BLUE}Adding squad member...${NC}"
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/squad/" \
         -H "Authorization: Bearer $ACTION_TOKEN" \
         -H "Content-Type: application/json" \
         -d "$DATA")

    HTTP_BODY=$(echo "$RESPONSE" | head -n -1)

    echo -e "${BLUE}Server response:${NC}"
    echo "$HTTP_BODY" | jq . 2>/dev/null || echo "$HTTP_BODY"
}

# ========== Post Team Need ==========
post_need() {
    if ! prompt_for_token; then return; fi

    read -p "Enter need description (or type 'cancel'): " CONTENT
    [[ "$CONTENT" == "cancel" ]] && echo -e "${RED}↩️  Cancelled.${NC}" && return

    DATA=$(jq -n --arg c "$CONTENT" '{content: $c}')

    echo -e "\n${BLUE}Posting team need...${NC}"
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/needs/" \
         -H "Authorization: Bearer $ACTION_TOKEN" \
         -H "Content-Type: application/json" \
         -d "$DATA")

    HTTP_BODY=$(echo "$RESPONSE" | head -n -1)

    echo -e "${BLUE}Server response:${NC}"
    echo "$HTTP_BODY" | jq . 2>/dev/null || echo "$HTTP_BODY"
}

# ========== Upload Photo ==========
upload_photo() {
    if ! prompt_for_token; then return; fi

    while true; do
        read -p "Enter full path to photo (or 'cancel'): " FILE_PATH
        [[ "$FILE_PATH" == "cancel" ]] && echo -e "${RED}↩️  Cancelled.${NC}" && return
        
        if [ -f "$FILE_PATH" ]; then
            break
        else
            echo -e "${RED}❌ File not found. Please try again.${NC}"
        fi
    done

    echo -e "\n${BLUE}Uploading photo...${NC}"
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/media/photos/" \
         -H "Authorization: Bearer $ACTION_TOKEN" \
         -F "photo=@$FILE_PATH")

    HTTP_BODY=$(echo "$RESPONSE" | head -n -1)

    echo -e "${BLUE}Server response:${NC}"
    echo "$HTTP_BODY" | jq . 2>/dev/null || echo "$HTTP_BODY"
}

# ========== Add Video Link ==========
add_video() {
    if ! prompt_for_token; then return; fi

    read -p "Enter YouTube URL (or type 'cancel'): " YT_LINK
    [[ "$YT_LINK" == "cancel" ]] && echo -e "${RED}↩️  Cancelled.${NC}" && return

    DATA=$(jq -n --arg yt "$YT_LINK" '{youtube_link: $yt}')

    echo -e "\n${BLUE}Adding video link...${NC}"
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/media/videos/" \
         -H "Authorization: Bearer $ACTION_TOKEN" \
         -H "Content-Type: application/json" \
         -d "$DATA")

    HTTP_BODY=$(echo "$RESPONSE" | head -n -1)

    echo -e "${BLUE}Server response:${NC}"
    echo "$HTTP_BODY" | jq . 2>/dev/null || echo "$HTTP_BODY"
}

# ========== Delete Photo ==========
delete_photo() {
    if ! prompt_for_token; then return; fi

    read -p "Enter Photo ID to delete (or type 'cancel'): " PHOTO_ID
    [[ "$PHOTO_ID" == "cancel" ]] && echo -e "${RED}↩️  Cancelled.${NC}" && return

    echo -e "\n${BLUE}Deleting photo...${NC}"
    RESPONSE=$(curl -s -w "\n%{http_code}" -X DELETE "$BASE_URL/api/media/photos/$PHOTO_ID/" \
         -H "Authorization: Bearer $ACTION_TOKEN")

    HTTP_BODY=$(echo "$RESPONSE" | head -n -1)

    echo -e "${BLUE}Server response:${NC}"
    echo "$HTTP_BODY" | jq . 2>/dev/null || echo "$HTTP_BODY"
}

# ========== Login for new tokens ==========
login() {
    read -p "Username: " USERNAME
    read -p "Password: " PASSWORD

    DATA=$(jq -n --arg u "$USERNAME" --arg p "$PASSWORD" \
      '{username: $u, password: $p}')

    echo -e "\n${BLUE}Logging in...${NC}"
    RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/login/" \
         -H "Content-Type: application/json" \
         -d "$DATA")

    HTTP_BODY=$(echo "$RESPONSE" | head -n -1)
    HTTP_CODE=$(echo "$RESPONSE" | tail -n 1)

    echo -e "${BLUE}Full response:${NC}"
    echo "$HTTP_BODY" | jq . 2>/dev/null || echo "$HTTP_BODY"

    ACCESS=$(echo "$HTTP_BODY" | jq -r '.access // empty')
    REFRESH=$(echo "$HTTP_BODY" | jq -r '.refresh // empty')

    if [[ -n "$ACCESS" ]]; then
        read -p "Save this access token for which team? " TEAM
        save_token "$TEAM" "$ACCESS"
        echo -e "${GREEN}✅ Access token saved for $TEAM${NC}"
        echo -e "${BLUE}Refresh Token:${NC} $REFRESH"
    else
        echo -e "${RED}❌ Login failed.${NC}"
    fi
}

# ========== Manually change token ==========
change_token() {
    read -p "Team Name: " TEAM
    read -p "Access Token: " TOKEN
    save_token "$TEAM" "$TOKEN"
    echo -e "${GREEN}✅ Token saved.${NC}"
}

# ========== Main Menu ==========
while true; do
    echo -e "\n${BLUE}========== Team Management Control Panel ==========${NC}"
    echo "   cancel → Type this at any prompt to return to main menu"
    echo "1) Add Team"
    echo "2) Add Staff Member"
    echo "3) Refresh Token"
    echo "4) Add Squad Member"
    echo "5) Login (Get new tokens)"
    echo "6) Change Access Token manually"
    echo "7) Post Team Need"
    echo "8) Upload Photo"
    echo "9) Add Video Link"
    echo "10) Delete Photo"
    echo "11) Exit"
    echo "===================================================="
    read -p "Select an option: " OPTION

    case $OPTION in
        1) add_team ;;
        2) add_staff ;;
        3) refresh_token ;;
        4) add_squad ;;
        5) login ;;
        6) change_token ;;
        7) post_need ;;
        8) upload_photo ;;
        9) add_video ;;
        10) delete_photo ;;
        11) echo "Goodbye!"; break ;;
        *) echo -e "${RED}Invalid option.${NC}" ;;
    esac
done