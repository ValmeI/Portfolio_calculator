#!/bin/bash

# URLs for different OS installers
declare -A DOWNLOAD_URLS=(
    [linux]="https://download2.interactivebrokers.com/installers/ibgateway/latest-standalone/ibgateway-latest-standalone-linux-x64.sh"
    [macos]="https://download2.interactivebrokers.com/installers/ibgateway/latest-standalone/ibgateway-latest-standalone-macos-arm.dmg"
)

# Detect operating system
get_os() {
    uname -s
}

# Get IB Gateway path for macOS
get_macos_paths() {
    echo "/Applications/IB Gateway 10.34"
    echo "$HOME/Applications/IB Gateway 10.34"
    echo "/Applications/IB Gateway"
    echo "$HOME/Applications/IB Gateway"
}

# Get IB Gateway path for Linux
get_linux_paths() {
    echo "/opt/ibgateway"
    echo "/usr/local/ibgateway"
    echo "$HOME/ibgateway"
}

# Check if IB Gateway is installed
is_ib_installed() {
    local os=$1
    local paths
    
    case "$os" in
        Darwin)
            paths=$(get_macos_paths)
            ;;
        Linux)
            paths=$(get_linux_paths)
            if command -v ibgateway >/dev/null 2>&1; then
                return 0
            fi
            ;;
        *)
            return 1
            ;;
    esac
    
    while IFS= read -r path; do
        if [ -d "$path" ]; then
            echo "✅ IB Gateway is already installed at: $path"
            return 0
        fi
    done <<< "$paths"
    
    return 1
}

# Cleanup function for temporary files
cleanup() {
    local installer=$1
    local os=$2
    
    case "$os" in
        Darwin)
            # For macOS, also detach any mounted volumes
            if mount | grep "/Volumes/IB Gateway" > /dev/null; then
                hdiutil detach "/Volumes/IB Gateway" -force 2>/dev/null
            fi
            ;;
    esac
    
    # Remove installer file if it exists
    [ -f "$installer" ] && rm -f "$installer"
}

# Get download URL and filename for the installer
get_installer_info() {
    local os=$1
    local downloads_dir="$HOME/Downloads"
    local url
    local output_file
    
    case "$os" in
        Darwin)
            url=${DOWNLOAD_URLS[macos]}
            output_file="$downloads_dir/ibgateway_installer.dmg"
            ;;
        Linux)
            url=${DOWNLOAD_URLS[linux]}
            output_file="$downloads_dir/ibgateway_installer.sh"
            ;;
        *)
            return 1
            ;;
    esac
    
    echo "$url $output_file"
}

# Download file using appropriate tool
download_file() {
    local url=$1
    local output_file=$2
    local os=$3
    
    echo "📥 Downloading IB Gateway for $os to $(dirname "$output_file")..."
    
    case "$os" in
        Darwin)
            if ! curl -L -o "$output_file" "$url"; then
                echo "❌ Failed to download macOS installer"
                return 1
            fi
            ;;
        Linux)
            if ! wget -O "$output_file" "$url"; then
                echo "❌ Failed to download Linux installer"
                return 1
            fi
            ;;
        *)
            return 1
            ;;
    esac
    
    return 0
}

# Verify downloaded file
verify_download() {
    local file=$1
    
    if [ ! -f "$file" ] || [ ! -s "$file" ]; then
        echo "❌ Downloaded file is missing or empty"
        return 1
    fi
    
    return 0
}

# Set file permissions
set_file_permissions() {
    local file=$1
    local os=$2
    
    case "$os" in
        Linux)
            chmod +x "$file"
            if [ ! -x "$file" ]; then
                echo "❌ Failed to set executable permissions"
                return 1
            fi
            echo "🔒 Set executable permissions for the installer"
            ;;
    esac
    
    return 0
}

# Main download function
download_installer() {
    local os=$1
    local installer_info
    local url
    local output_file
    
    # Get installer info
    installer_info=$(get_installer_info "$os") || return 1
    read -r url output_file <<< "$installer_info"
    
    # Download the file
    if ! download_file "$url" "$output_file" "$os"; then
        return 1
    fi
    
    # Verify the download
    if ! verify_download "$output_file"; then
        return 1
    fi
    
    # Set permissions if needed
    if ! set_file_permissions "$output_file" "$os"; then
        return 1
    fi
    
    echo "✅ Successfully downloaded IB Gateway installer"
    echo "$output_file"
    return 0
}

# Check installer file size
check_installer_size() {
    local file=$1
    local size
    
    if [ "$(uname -s)" = "Darwin" ]; then
        size=$(stat -f %z "$file")
    else
        size=$(stat -c %s "$file")
    fi
    
    echo "📋 File size: $size bytes"
    
    if [ "$size" -lt 1000000 ]; then
        echo "❌ The downloaded file is too small to be a valid installer"
        echo "📝 Please download the installer manually:"
        echo "1. Visit https://www.interactivebrokers.com/en/trading/ibgateway-latest.php"
        echo "2. Log in to your IBKR account"
        echo "3. Download the installer for your OS"
        echo "4. Move the downloaded file to $(pwd)/$file"
        echo "5. Run this script again"
        rm -f "$file"
        return 1
    fi
    
    return 0
}

# Install on Linux
install_linux() {
    local installer=$1
    
    echo "🚀 Installing IB Gateway..."
    
    # Try to install without sudo first
    if "$installer" --mode unattended; then
        echo "✅ Installation completed successfully"
        return 0
    else
        echo "ℹ️ Attempting installation with sudo..."
        if ! sudo "$installer" --mode unattended; then
            echo "❌ Installation failed"
            return 1
        fi
        echo "✅ Installation completed successfully with sudo"
        return 0
    fi
    
    rm -f "$installer"
    return 0
}

# Install on macOS
install_macos() {
    local installer=$1
    
    echo "🚀 Installing IB Gateway..."
    MOUNT_OUTPUT=$(hdiutil attach "$installer")
    MOUNT_POINT=$(echo "$MOUNT_OUTPUT" | grep "/Volumes/" | sed 's/.*\/Volumes\//\/Volumes\//g')
    
    if [ -z "$MOUNT_POINT" ]; then
        echo "❌ Failed to find the mounted volume"
        rm -f "$installer"
        return 1
    fi
    
    echo "💾 Mounted disk image at: $MOUNT_POINT"
    echo "📂 Contents of mount point:"
    ls -la "$MOUNT_POINT"
    
    INSTALLER_APP=$(find "$MOUNT_POINT" -name "*Installer.app" -maxdepth 1 2>/dev/null)
    
    if [ -z "$INSTALLER_APP" ]; then
        echo "❌ Could not find the installer application"
        hdiutil detach "$MOUNT_POINT" -force 2>/dev/null
        rm -f "$installer"
        return 1
    fi
    
    echo "🔍 Found installer at: $INSTALLER_APP"
    echo "📦 Running IB Gateway installer..."
    open "$INSTALLER_APP"
    
    echo "ℹ️ Please complete the installation using the installer window."
    echo "📙 Installation Instructions:"
    echo "1. Click 'Next' to start the installation"
    echo "2. Accept the license agreement"
    echo "3. Choose the installation location (recommended: /Applications)"
    echo "4. Complete the installation"
    echo "5. After installation is complete, you can close the installer"
    
    read -p "✅ Press Enter after completing the installation..."
    
    echo "🧹 Cleaning up..."
    hdiutil detach "$MOUNT_POINT" || hdiutil detach "$MOUNT_POINT" -force 2>/dev/null
    rm -f "$installer"
    return 0
}

# Main execution
main() {
    local os=$(get_os)
    echo "🔍 Detected OS: $os"
    
    if is_ib_installed "$os"; then
        echo "🔹 No need to install IB Gateway."
        exit 0
    fi
    
    # Set up cleanup trap
    trap 'cleanup "$installer_file" "$os"' EXIT
    
    local installer_file
    installer_file=$(download_installer "$os" | tail -n1)
    download_status=$?
    
    if [ $download_status -eq 0 ] && [ -n "$installer_file" ] && [ -f "$installer_file" ] && [ -x "$installer_file" ]; then
        echo "📦 Using installer: $installer_file"
    else
        exit 1
    fi
    
    if ! check_installer_size "$installer_file"; then
        exit 1
    fi
    
    
    case "$os" in
        Linux)
            if ! install_linux "$installer_file"; then
                echo "❌ Installation failed on Linux"
                exit 1
            fi
            ;;
        Darwin)
            if ! install_macos "$installer_file"; then
                echo "❌ Installation failed on macOS"
                exit 1
            fi
            ;;
        *)
            echo "❌ Unsupported OS: $os (only Linux and macOS are supported)"
            exit 1
            ;;
    esac
}

# Run main function
main

echo "✅ IB Gateway installation completed!"
