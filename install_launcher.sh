#!/bin/bash
# Installation script for xdfgui launcher
# This script creates a clickable launcher in ~/Applications/

XDFGUI_PATH=~/code/xdfgui

# Create a .app bundle for xdfgui
mkdir -p "$HOME/Applications/xdfgui.app/Contents/MacOS"

# Create the launcher script inside the app bundle
cat > "$HOME/Applications/xdfgui.app/Contents/MacOS/xdfgui" << 'EOF'
#!/bin/bash
cd ~/code/xdfgui
uv run xdfgui
EOF

chmod +x "$HOME/Applications/xdfgui.app/Contents/MacOS/xdfgui"

# Create Info.plist for the app bundle
cat > "$HOME/Applications/xdfgui.app/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleExecutable</key>
    <string>xdfgui</string>
    <key>CFBundleIdentifier</key>
    <string>com.xdfgui.app</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>xdfgui</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>0.1.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF

echo "✅ xdfgui launcher created at ~/Applications/xdfgui.app"
echo "You can now open it from Finder or Spotlight (Cmd+Space, type 'xdfgui')"
