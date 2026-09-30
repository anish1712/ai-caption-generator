import requests
import json
import urllib3

# SSL એરર બાયપાસ કરવા માટે
urllib3.disable_warnings()

print("\n" + "="*50)
print(" 📸 AI Instagram Caption Generator (Direct API Version)")
print("="*50)

api_key = input("\nતમારી Google Gemini API Key નાખો: ").strip()

print("\n✅ API Key સેટ થઈ ગઈ છે!\n")

while True:
    topic = input("તમારો ફોટો શેના વિશે છે? (બંધ કરવા 'exit' લખો): ").strip()
    
    if topic.lower() == 'exit':
        print("આવજો! 👋")
        break
        
    if not topic:
        print("❌ કંઈક તો લખવું પડશે ને!")
        continue
        
    print("⏳ કેપ્શન બની રહ્યું છે... (રાહ જુઓ)")
    
    prompt = f"Write an engaging Instagram caption for a photo about '{topic}'. Include relevant trending hashtags and emojis. If the topic is written in Gujarati, give the output caption in Gujarati. If English or Hindi, use that respective language."
    
    # સીધી Google ની API ને રિક્વેસ્ટ મોકલો
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        # verify=False એટલે SSL ચેક નહીં કરે
        response = requests.post(url, headers=headers, json=data, verify=False)
        result = response.json()
        
        if response.status_code == 200:
            caption = result['candidates'][0]['content']['parts'][0]['text']
            print("\n" + "-"*40)
            print("✨ તમારું કેપ્શન ✨")
            print("-"*40)
            print(caption.strip())
            print("-"*40 + "\n")
        else:
            print("\n❌ Google તરફથી એરર આવી છે:")
            print(result)
            
    except Exception as e:
        print("\n❌ નેટવર્ક અથવા બીજી કોઈ એરર છે: ", e)
