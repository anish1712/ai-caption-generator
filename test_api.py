import google.generativeai as genai
import time

print("--- AI Speed Test ---")
api_key = input("અહીં તમારી API Key પેસ્ટ કરો અને Enter દબાવો: ").strip()

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    print("\nAI ને પ્રશ્ન મોકલી રહ્યા છીએ... રાહ જુઓ...")
    start_time = time.time()
    
    response = model.generate_content("Say hello in Gujarati")
    
    end_time = time.time()
    
    print("\nજવાબ:", response.text.strip())
    print(f"\n[રિઝલ્ટ] જવાબ આવવામાં માત્ર {end_time - start_time:.2f} સેકન્ડનો સમય લાગ્યો.")
except Exception as e:
    print("\nએરર આવી છે:", e)
