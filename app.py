import streamlit as st
from portfolio_visuals import render_visuals
FAQ = {
    "refund": "I can help explain the refund process. Please share the order reference through the approved support channel. A human agent must confirm eligibility and timing.",
    "login": "Try resetting your password using the official sign-in page. Never share your password or one-time passcode with support.",
    "delivery": "Check the latest tracking status from the official order page. If tracking has not updated, a human agent may need to investigate."
}

def classify(message: str) -> str:
    text = message.lower()
    for key in FAQ:
        if key in text:
            return key
    return "other"

def draft_reply(message: str) -> dict:
    category = classify(message)
    answer = FAQ.get(category, "Thanks for contacting support. I need a little more detail to route this correctly. A support agent should review this case.")
    return {"category": category, "draft": answer, "needs_human_review": category == "other" or any(w in message.lower() for w in ["angry", "legal", "chargeback", "urgent"])}

st.set_page_config(page_title="Customer Support AI", page_icon="ðŸ’¬")
render_visuals('01_customer_support_agent')
st.title("Customer Support AI Agent")
st.caption("Demo only: replies are drafts, not sent messages.")
message = st.text_area("Customer message", placeholder="Example: I need help with my refund")
if st.button("Classify and draft", type="primary"):
    if not message.strip():
        st.warning("Enter a message first.")
    else:
        result = draft_reply(message)
        st.write("**Category:**", result["category"])
        st.write("**Draft reply:**", result["draft"])
        st.write("**Human review required:**", "Yes" if result["needs_human_review"] else "Review if policy requires")

