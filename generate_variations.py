import json
import os

# Paths
INPUT_PATH = 'data/raw/Ecommerce_FAQ_Chatbot_dataset.json'
OUTPUT_PATH = 'data/raw/Ecommerce_FAQ_Chatbot_dataset_augmented.json'

# This dictionary maps the EXACT original question to a list of variations
# I have added variations for ALL questions based on your request.
VARIATIONS_MAP = {
    "How can I create an account?": [
        "how to sign up", "create account", "register new account", "sign up", "start account", "registration", "make an account", "new user signup"
    ],
    "What payment methods do you accept?": [
        "how can i pay", "payment options", "do you take credit cards", "paypal accepted?", "payment types", "cards accepted", "paying for order"
    ],
    "How can I track my order?": [
        "where is my stuff", "track order", "order status", "shipping status", "package location", "tracking number", "where is my package", "check order"
    ],
    "What is your return policy?": [
        "can i return this", "return rules", "how to return", "refund policy", "returns", "exchange policy", "30 day return"
    ],
    "Can I cancel my order?": [
        "stop my order", "cancel purchase", "cancel shipment", "dont want it anymore", "how to cancel", "cancel item"
    ],
    "How long does shipping take?": [
        "shipping time", "delivery time", "when will it arrive", "how fast is shipping", "delivery speed", "shipping duration"
    ],
    "Do you offer international shipping?": [
        "ship to other countries", "shipping abroad", "international delivery", "global shipping", "ship outside us", "foreign shipping"
    ],
    "What should I do if my package is lost or damaged?": [
        "lost package", "broken item", "damaged in transit", "package missing", "never arrived", "received damaged goods", "shipment lost"
    ],
    "Can I change my shipping address after placing an order?": [
        "wrong address", "update shipping address", "change delivery location", "edit address", "fix address", "shipped to wrong place"
    ],
    "How can I contact customer support?": [
        "talk to someone", "customer service number", "help desk", "contact us", "support email", "phone number", "need help"
    ],
    "Do you offer gift wrapping services?": [
        "wrap as gift", "gift wrap", "gift options", "sending as present", "wrapping paper"
    ],
    "What is your price matching policy?": [
        "match price", "price match", "lower price elsewhere", "competitor price", "price guarantee"
    ],
    "Can I order by phone?": [
        "call to order", "phone order", "place order over phone", "telephone order"
    ],
    "Are my personal and payment details secure?": [
        "is this safe", "security", "data privacy", "credit card safe", "secure checkout", "safe to pay"
    ],
    "What is your price adjustment policy?": [
        "price dropped", "sale after purchase", "price adjustment", "refund difference", "price went down"
    ],
    "Do you have a loyalty program?": [
        "rewards program", "earn points", "loyalty points", "membership benefits", "rewards club", "join loyalty"
    ],
    "Can I order without creating an account?": [
        "guest checkout", "buy as guest", "no account needed", "guest order", "checkout without login"
    ],
    "Do you offer bulk or wholesale discounts?": [
        "buy in bulk", "wholesale price", "volume discount", "large order discount", "business pricing", "bulk buy"
    ],
    "Can I change or cancel an item in my order?": [
        "remove item", "edit order", "change item", "modify order", "delete product from order"
    ],
    "How can I leave a product review?": [
        "write review", "rate product", "give feedback", "product rating", "submit review", "where to review"
    ],
    "Can I use multiple promo codes on a single order?": [
        "stack coupons", "two promo codes", "multiple discounts", "use two codes", "coupon stacking"
    ],
    "What should I do if I receive the wrong item?": [
        "wrong product sent", "incorrect item", "sent wrong thing", "mistake in order", "not what i ordered"
    ],
    "Do you offer expedited shipping?": [
        "fast shipping", "express delivery", "overnight shipping", "rush delivery", "next day shipping"
    ],
    "Can I order a product that is out of stock?": [
        "buy out of stock", "backorder", "when back in stock", "notify when available", "item unavailable"
    ],
    "What is your email newsletter about?": [
        "subscribe to email", "newsletter content", "email updates", "mailing list"
    ],
    "Can I return a product if I changed my mind?": [
        "dont like it", "changed mind", "return no reason", "buyers remorse", "return unwanted item"
    ],
    "Do you offer live chat support?": [
        "chat with support", "live help", "chat online", "talk to agent now", "online chat"
    ],
    "Can I order a product as a gift?": [
        "send as gift", "gift receipt", "buying for someone else", "ship to friend"
    ],
    "What should I do if my discount code is not working?": [
        "promo code failed", "coupon invalid", "code wont work", "discount error", "code not applying"
    ],
    "Can I return a product if it was a final sale item?": [
        "return clearance", "return final sale", "refund sale item", "non returnable"
    ],
    "Do you offer installation services for your products?": [
        "install it for me", "setup service", "installation help", "do you install", "assembly service"
    ],
    "Can I order a product that is discontinued?": [
        "buy old product", "discontinued item", "out of production", "find old model"
    ],
    "Can I return a product without a receipt?": [
        "lost receipt", "no proof of purchase", "return without invoice", "missing receipt"
    ],
    "Can I order a product for delivery to a different country?": [
        "ship overseas", "delivery to another country", "international order"
    ],
    "Can I add a gift message to my order?": [
        "write note", "gift card message", "personal message", "include note"
    ],
    "Can I request a product demonstration before making a purchase?": [
        "see product demo", "demo request", "try before buy", "show me how it works"
    ],
    "Can I order a product that is listed as 'coming soon'?": [
        "buy coming soon", "prepurchase", "order upcoming item"
    ],
    "Can I request an invoice for my order?": [
        "get bill", "download invoice", "need receipt", "tax invoice"
    ],
    "Can I order a product that is labeled as 'limited edition'?": [
        "buy limited edition", "special edition", "exclusive item"
    ],
    "Can I return a product if I no longer have the original packaging?": [
        "no box return", "threw away box", "missing packaging", "return without box"
    ],
    "Can I request a product that is currently out of stock to be reserved for me?": [
        "hold item", "reserve product", "save for me", "booking item"
    ],
    "Can I order a product that is listed as 'pre-order' with other in-stock items?": [
        "mixed order", "preorder and normal item", "combine shipping"
    ],
    "Can I return a product if it was damaged during shipping?": [
        "arrived broken", "shipping damage", "courier broke it", "damaged delivery"
    ],
    "Can I request a product that is out of stock to be restocked?": [
        "restock request", "bring it back", "when will you have more"
    ],
    "Can I order a product if it is listed as 'backordered'?": [
        "buy backorder", "purchase backordered", "wait for stock"
    ],
    "Can I return a product if it was purchased during a sale or with a discount?": [
        "return sale item", "return discounted", "refund on sale"
    ],
    "Can I request a product repair or replacement if it is damaged?": [
        "fix broken item", "repair service", "replace damaged", "warranty claim"
    ],
    "Can I order a product if it is listed as 'out of stock' but available for pre-order?": [
        "preorder out of stock", "reserve out of stock"
    ],
    "Can I return a product if it was purchased as a gift?": [
        "return gift", "gift return", "received as gift", "dont want gift"
    ],
    "Can I request a product if it is listed as 'discontinued'?": [
        "request discontinued", "find discontinued", "order old stock"
    ],
    "Can I order a product if it is listed as 'sold out'?": [
        "buy sold out", "purchase sold out"
    ],
    "Can I return a product if it was purchased with a gift card?": [
        "return gift card purchase", "refund to gift card"
    ],
    "Can I request a product if it is not currently available in my size?": [
        "size out of stock", "wrong size available", "need different size"
    ],
    "Can I order a product if it is listed as 'coming soon' but available for pre-order?": [
        "preorder coming soon", "order future item"
    ],
    "Can I return a product if it was purchased with a discount code?": [
        "return with coupon", "refund promo code"
    ],
    "Can I request a custom order or personalized product?": [
        "custom made", "personalize item", "custom order", "make it unique"
    ],
    "Can I order a product if it is listed as 'temporarily unavailable'?": [
        "buy unavailable", "order temp out of stock"
    ],
    "Can I return a product if it was damaged due to improper use?": [
        "i broke it", "accidental damage", "user damage return"
    ],
    "Can I request a product if it is listed as 'coming soon' but not available for pre-order?": [
        "wait for coming soon", "when can i buy coming soon"
    ],
    "Can I order a product if it is listed as 'on hold'?": [
        "buy on hold", "order held item"
    ],
    "Can I return a product if I no longer have the original receipt?": [
        "lost receipt return", "return no invoice", "missing proof of purchase"
    ],
    "Can I request a product that is listed as 'limited edition' to be restocked?": [
        "restock limited edition", "more limited items"
    ],
    "Can I order a product if it is listed as 'discontinued' but still visible on the website?": [
        "buy discontinued website", "visible but discontinued"
    ],
    "Can I return a product if it was a clearance or final sale item?": [
        "return clearance", "refund final sale"
    ],
    "Can I request a product if it is not listed on your website?": [
        "product not found", "cant find item", "special request"
    ],
    "Can I order a product if it is listed as 'out of stock' but available for backorder?": [
        "backorder out of stock", "buy backordered"
    ],
    "Can I return a product if it was purchased as part of a bundle or set?": [
        "return bundle", "return part of set", "split bundle return"
    ],
    "Can I request a product that is listed as 'out of stock' to be restocked?": [
        "notify restock", "when restock"
    ],
    "Can I order a product if it is listed as 'coming soon' and available for pre-order?": [
        "preorder soon", "buy upcoming"
    ],
    "Can I return a product if it was damaged due to mishandling during shipping?": [
        "courier damage", "shipping damage return"
    ],
    "Can I request a product that is listed as 'out of stock' to be reserved for me?": [
        "reserve stock", "hold for me"
    ],
    "Can I order a product if it is listed as 'pre-order' but available for backorder?": [
        "preorder backorder", "waitlist"
    ],
    "Can I return a product if it was purchased with store credit?": [
        "return store credit", "refund credit"
    ],
    "Can I request a product that is currently out of stock to be restocked?": [
        "restock please", "bring back item"
    ],
    "Can I order a product if it is listed as 'sold out' but available for pre-order?": [
        "preorder sold out", "buy sold out item"
    ],
    "Can I return a product if it was purchased with a promotional gift card?": [
        "return promo card", "refund promo gift card"
    ],
    "Can I request a product if it is not currently available in my preferred color?": [
        "color out of stock", "want different color"
    ],
    "Can I order a product if it is listed as 'coming soon' and not available for pre-order?": [
        "buy coming soon item"
    ],
    "Can I return a product if it was purchased during a promotional event?": [
        "return promo item", "refund event purchase"
    ]
}

def generate_augmented_data():
    print(f"Loading data from {INPUT_PATH}...")
    try:
        with open(INPUT_PATH, 'r') as f:
            data = json.load(f)
            
        questions = data.get('questions', [])
        print(f"Found {len(questions)} original questions.")
        
        # Inject variations
        augmented_count = 0
        for entry in questions:
            q_text = entry['question']
            if q_text in VARIATIONS_MAP:
                entry['variations'] = VARIATIONS_MAP[q_text]
                augmented_count += 1
            else:
                # Debugging: Print which questions I might have missed (should be none)
                print(f"Warning: No variations found for: {q_text}")
                
        # Save new file
        print(f"Injecting variations for {augmented_count} questions...")
        
        # Wrap it back in the 'questions' key structure
        output_data = {'questions': questions}
        
        with open(OUTPUT_PATH, 'w') as f:
            json.dump(output_data, f, indent=4)
            
        print(f"Success! Augmented data saved to {OUTPUT_PATH}")
        
    except FileNotFoundError:
        print("Error: Could not find the input JSON file. Check the path.")

if __name__ == "__main__":
    generate_augmented_data()