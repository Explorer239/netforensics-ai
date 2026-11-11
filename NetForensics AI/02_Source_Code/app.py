# ============================================================
# NETFORENSICS AI
# AI-Assisted Network Fault Diagnosis and Human Review System
# ============================================================

import streamlit as st
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="NetForensics AI",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# Uses Streamlit theme colors automatically
# ============================================================

css = (
    "<style>"

    ".block-container {"
    "max-width: 1100px;"
    "padding-top: 2rem;"
    "padding-bottom: 3rem;"
    "}"

    ".hero {"
    "text-align: center;"
    "padding: 28px 20px;"
    "border-radius: 20px;"
    "margin-bottom: 20px;"
    "background-color: var(--secondary-background-color);"
    "border: 1px solid rgba(128,128,128,0.25);"
    "box-shadow: 0px 8px 25px rgba(0,0,0,0.08);"
    "}"

    ".hero h1 {"
    "font-size: 48px;"
    "font-weight: 800;"
    "color: var(--text-color);"
    "margin-bottom: 8px;"
    "}"

    ".subtitle {"
    "font-size: 18px;"
    "color: var(--text-color);"
    "opacity: 0.75;"
    "}"

    ".card {"
    "background-color: var(--secondary-background-color);"
    "color: var(--text-color);"
    "border: 1px solid rgba(128,128,128,0.25);"
    "border-radius: 18px;"
    "padding: 20px;"
    "min-height: 130px;"
    "box-shadow: 0px 6px 20px rgba(0,0,0,0.06);"
    "transition: transform 0.2s ease;"
    "}"

    ".card:hover {"
    "transform: translateY(-4px);"
    "}"

    ".card h3 {"
    "color: var(--text-color);"
    "}"

    ".card p {"
    "color: var(--text-color);"
    "opacity: 0.75;"
    "}"

    "[data-testid='stSidebar'] {"
    "border-right: 1px solid rgba(128,128,128,0.15);"
    "}"

    "[data-testid='stChatMessage'] {"
    "border-radius: 16px;"
    "}"

    "</style>"
)

st.markdown(css, unsafe_allow_html=True)


# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

@st.cache_data
def load_data():

    try:
        data = pd.read_csv("human_review_results.csv")
        return data

    except Exception:
        return pd.DataFrame()


df = load_data()


# ============================================================
# PREPARE SIMILARITY SEARCH
# ============================================================

vectorizer = None
case_vectors = None


if not df.empty:

    search_columns = [
        "Protocol",
        "Symptom",
        "Evidence",
        "Expected_Fault",
        "Fault",
        "Root_Cause"
    ]

    available_columns = []

    for column in search_columns:

        if column in df.columns:
            available_columns.append(column)

    if len(available_columns) > 0:

        df = df.copy()

        df["search_text"] = (
            df[available_columns]
            .fillna("")
            .astype(str)
            .agg(" ".join, axis=1)
        )

        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2)
        )

        case_vectors = vectorizer.fit_transform(
            df["search_text"]
        )


# ============================================================
# SAFE COLUMN VALUE
# ============================================================

def get_value(row, possible_columns):

    if row is None:
        return "Not Available"

    for column in possible_columns:

        if column in row.index:

            value = row[column]

            if pd.notna(value):
                return str(value)

    return "Not Available"


# ============================================================
# FIND SIMILAR CASE
# ============================================================

def find_similar_case(user_input):

    if vectorizer is None:
        return None, 0

    if case_vectors is None:
        return None, 0

    if df.empty:
        return None, 0

    user_vector = vectorizer.transform([user_input])

    scores = cosine_similarity(
        user_vector,
        case_vectors
    )[0]

    best_index = scores.argmax()
    best_score = scores[best_index]

    return best_index, best_score


# ============================================================
# RULE-BASED NETWORK FAULT DETECTION
# ============================================================

def detect_fault(text):

    text = text.lower()


    # --------------------------------------------------------
    # INTERFACE DOWN
    # --------------------------------------------------------

    if (
        "administratively down" in text
        or "interface down" in text
        or "port down" in text
    ):

        return {
            "fault": "Interface Administratively Down",
            "protocol": "Network Interface",
            "layer": "Physical Layer - Layer 1",
            "reason": (
                "The network interface has been manually disabled "
                "and cannot forward network traffic."
            ),
            "verification": "show ip interface brief",
            "steps": [
                "Check the current interface status.",
                "Enter configuration mode.",
                "Select the affected interface.",
                "Enable the interface using no shutdown.",
                "Verify that the interface becomes up."
            ],
            "commands": [
                "enable",
                "configure terminal",
                "interface <interface_name>",
                "no shutdown",
                "end",
                "show ip interface brief"
            ],
            "confidence": 95
        }


    # --------------------------------------------------------
    # VLAN
    # --------------------------------------------------------

    if (
        "vlan mismatch" in text
        or "wrong vlan" in text
        or "vlan issue" in text
        or "vlan problem" in text
    ):

        return {
            "fault": "Incorrect VLAN Configuration",
            "protocol": "VLAN",
            "layer": "Data Link Layer - Layer 2",
            "reason": (
                "The switch port may be assigned to the wrong VLAN "
                "or the required VLAN may not be configured."
            ),
            "verification": "show vlan brief",
            "steps": [
                "Check existing VLAN configuration.",
                "Identify the affected switch port.",
                "Verify the correct VLAN number.",
                "Assign the correct VLAN to the port.",
                "Verify VLAN membership.",
                "Test connectivity again."
            ],
            "commands": [
                "enable",
                "show vlan brief",
                "configure terminal",
                "interface fa0/1",
                "switchport mode access",
                "switchport access vlan <vlan_number>",
                "end"
            ],
            "confidence": 92
        }


    # --------------------------------------------------------
    # DHCP
    # --------------------------------------------------------

    if (
        "169.254" in text
        or "dhcp failed" in text
        or "dhcp timeout" in text
        or "unable to obtain ip" in text
        or "dhcp problem" in text
    ):

        return {
            "fault": "DHCP Address Assignment Failure",
            "protocol": "DHCP",
            "layer": "Application Layer",
            "reason": (
                "The client cannot obtain a valid IP address "
                "from the DHCP server."
            ),
            "verification": "show ip dhcp binding",
            "steps": [
                "Check connectivity to the DHCP server.",
                "Verify the DHCP address pool.",
                "Check VLAN connectivity.",
                "Verify DHCP service configuration.",
                "Renew the client IP address."
            ],
            "commands": [
                "show ip dhcp pool",
                "show ip dhcp binding",
                "ipconfig /release",
                "ipconfig /renew"
            ],
            "confidence": 93
        }


    # --------------------------------------------------------
    # DNS
    # --------------------------------------------------------

    if (
        "dns" in text
        or "nslookup" in text
        or "cannot resolve" in text
        or "name resolution" in text
    ):

        return {
            "fault": "DNS Resolution Failure",
            "protocol": "DNS",
            "layer": "Application Layer",
            "reason": (
                "The DNS server may be unreachable, incorrectly "
                "configured, or unable to resolve the requested domain."
            ),
            "verification": "nslookup <domain_name>",
            "steps": [
                "Check the configured DNS server.",
                "Verify connectivity to the DNS server.",
                "Verify that DNS service is running.",
                "Check DNS records.",
                "Test name resolution again."
            ],
            "commands": [
                "ipconfig /all",
                "ping <dns_server_ip>",
                "nslookup <domain_name>"
            ],
            "confidence": 91
        }


    # --------------------------------------------------------
    # OSPF
    # --------------------------------------------------------

    if (
        "ospf neighbor" in text
        or "ospf adjacency" in text
        or "ospf not forming" in text
        or "ospf problem" in text
    ):

        return {
            "fault": "OSPF Neighbor Adjacency Failure",
            "protocol": "OSPF",
            "layer": "Network Layer - Layer 3",
            "reason": (
                "OSPF neighbors may have mismatched area IDs, "
                "timers, authentication settings, or network configurations."
            ),
            "verification": "show ip ospf neighbor",
            "steps": [
                "Check connectivity between routers.",
                "Verify IP addresses.",
                "Check OSPF area IDs.",
                "Verify OSPF network statements.",
                "Check hello and dead timers.",
                "Verify neighbor status again."
            ],
            "commands": [
                "show ip ospf neighbor",
                "show ip ospf interface brief",
                "show ip protocols",
                "show running-config"
            ],
            "confidence": 92
        }


    # --------------------------------------------------------
    # ROUTING
    # --------------------------------------------------------

    if (
        "network unreachable" in text
        or "no route to host" in text
        or "route not found" in text
        or "missing route" in text
        or "routing problem" in text
    ):

        return {
            "fault": "Missing or Incorrect Route",
            "protocol": "IP Routing",
            "layer": "Network Layer - Layer 3",
            "reason": (
                "The router does not have a valid route "
                "to reach the destination network."
            ),
            "verification": "show ip route",
            "steps": [
                "Check the routing table.",
                "Identify the missing destination network.",
                "Verify the next-hop address.",
                "Add or correct the route.",
                "Verify the routing table.",
                "Test connectivity."
            ],
            "commands": [
                "show ip route",
                "show ip interface brief",
                "ip route <destination_network> <subnet_mask> <next_hop>"
            ],
            "confidence": 90
        }


    # --------------------------------------------------------
    # ARP
    # --------------------------------------------------------

    if (
        "arp" in text
        or "incomplete arp" in text
    ):

        return {
            "fault": "ARP Resolution Failure",
            "protocol": "ARP",
            "layer": "Data Link Layer - Layer 2",
            "reason": (
                "The device cannot correctly resolve the destination "
                "IP address to a MAC address."
            ),
            "verification": "show arp",
            "steps": [
                "Check Layer 2 connectivity.",
                "Verify VLAN configuration.",
                "Check the ARP table.",
                "Clear stale ARP entries if necessary.",
                "Test connectivity again."
            ],
            "commands": [
                "show arp",
                "show vlan brief",
                "ping <destination_ip>"
            ],
            "confidence": 87
        }


    # --------------------------------------------------------
    # PING FAILURE
    # --------------------------------------------------------

    if (
        "request timed out" in text
        or "100% packet loss" in text
        or "destination host unreachable" in text
        or "ping failed" in text
    ):

        return {
            "fault": "Network Connectivity Failure",
            "protocol": "IP Connectivity",
            "layer": "Multiple Layers - Investigation Required",
            "reason": (
                "The destination cannot be reached because of a possible "
                "physical, VLAN, IP addressing, gateway, or routing issue."
            ),
            "verification": "show ip interface brief",
            "steps": [
                "Check physical cable connections.",
                "Verify interface status.",
                "Check IP address and subnet mask.",
                "Verify default gateway.",
                "Check VLAN configuration.",
                "Verify routing configuration.",
                "Test connectivity hop by hop."
            ],
            "commands": [
                "show ip interface brief",
                "show vlan brief",
                "show ip route",
                "ping <gateway_ip>"
            ],
            "confidence": 75
        }


    return None


# ============================================================
# ANALYZE NETWORK FAULT
# ============================================================

def analyze_fault(user_input):

    rule_result = detect_fault(user_input)

    similar_index, similarity_score = find_similar_case(
        user_input
    )


    if rule_result is not None:

        if similar_index is not None:

            matched_case = df.iloc[similar_index]

            rule_result["similar_case"] = get_value(
                matched_case,
                ["Case_ID", "Case ID", "ID"]
            )

        else:

            rule_result["similar_case"] = (
                "Rule-based diagnosis"
            )

        return rule_result


    if similar_index is not None:

        matched_case = df.iloc[similar_index]

        confidence = round(
            similarity_score * 100,
            1
        )

        return {
            "fault": get_value(
                matched_case,
                [
                    "Expected_Fault",
                    "Fault",
                    "Root_Cause"
                ]
            ),

            "protocol": get_value(
                matched_case,
                ["Protocol"]
            ),

            "layer": "Further Verification Required",

            "reason": (
                "The input was matched with the closest "
                "case in the troubleshooting knowledge base."
            ),

            "verification": get_value(
                matched_case,
                [
                    "Expected_Next_Command",
                    "Recommended_Command",
                    "Next_Command"
                ]
            ),

            "steps": [
                get_value(
                    matched_case,
                    [
                        "Suggested_Fix",
                        "Fix",
                        "Resolution"
                    ]
                ),
                "Run the verification command.",
                "Verify the network configuration.",
                "Test connectivity again."
            ],

            "commands": [
                "show ip interface brief",
                "show vlan brief",
                "show ip route"
            ],

            "confidence": confidence,

            "similar_case": get_value(
                matched_case,
                ["Case_ID", "Case ID", "ID"]
            )
        }


    return {
        "fault": "Specific Fault Not Identified",
        "protocol": "Unknown",
        "layer": "Further Investigation Required",
        "reason": (
            "The provided information is insufficient "
            "to confidently identify a specific network fault."
        ),
        "verification": "show ip interface brief",
        "steps": [
            "Check physical connectivity.",
            "Check interface status.",
            "Verify IP addressing.",
            "Check VLAN configuration.",
            "Verify routing."
        ],
        "commands": [
            "show ip interface brief",
            "show vlan brief",
            "show ip route"
        ],
        "confidence": 25,
        "similar_case": "No matching case found"
    }


# ============================================================
# HUMAN REVIEW DECISION
# ============================================================

def get_human_review_status(confidence):

    if confidence >= 80:

        return {
            "status": "🟢 Auto Diagnosis Approved",
            "message": (
                "High AI confidence. The diagnosis can be used as "
                "a strong recommendation, although final verification "
                "by a network administrator is always recommended."
            ),
            "review_required": False
        }


    elif confidence >= 50:

        return {
            "status": "🟡 Human Review Recommended",
            "message": (
                "The AI has moderate confidence. A network administrator "
                "should verify the diagnosis before applying changes."
            ),
            "review_required": True
        }


    else:

        return {
            "status": "🔴 Human Review Required",
            "message": (
                "The AI confidence is low. The diagnosis should not be "
                "applied automatically. A network administrator should "
                "investigate the issue manually."
            ),
            "review_required": True
        }


# ============================================================
# USER INTENT DETECTION
# ============================================================

def detect_user_intent(user_input):

    text = user_input.lower().strip()

    greetings = [
        "hi",
        "hello",
        "hey",
        "hii",
        "hiii",
        "good morning",
        "good afternoon",
        "good evening"
    ]

    thanks = [
        "thanks",
        "thank you",
        "thx",
        "thankyou"
    ]

    diagnosis_keywords = [
        "error",
        "fault",
        "problem",
        "issue",
        "diagnose",
        "diagnosis",
        "not working",
        "failed",
        "failure",
        "down",
        "unreachable",
        "timeout",
        "packet loss",
        "ping",
        "vlan",
        "dhcp",
        "dns",
        "ospf",
        "routing",
        "route",
        "interface",
        "arp",
        "network error",
        "connection failed",
        "request timed out",
        "destination host unreachable"
    ]

    if text in greetings:
        return "greeting"

    if text in thanks:
        return "thanks"

    for keyword in diagnosis_keywords:

        if keyword in text:
            return "diagnosis"

    return "general"


# ============================================================
# SESSION STATE
# ============================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🌐 NetForensics AI")

    st.caption(
        "AI-Assisted Network Troubleshooting"
    )

    st.divider()

    st.success(
        "🟢 AI Diagnosis Engine Online"
    )

    if not df.empty:

        st.metric(
            "Knowledge Base Cases",
            len(df)
        )

        if "Protocol" in df.columns:

            st.metric(
                "Protocols Available",
                df["Protocol"].nunique()
            )

    st.divider()

    st.subheader("How It Works")

    st.write(
        "1. Create or simulate a network fault."
    )

    st.write(
        "2. Run troubleshooting commands."
    )

    st.write(
        "3. Copy the error or symptom."
    )

    st.write(
        "4. Submit it to NetForensics AI."
    )

    st.write(
        "5. Review AI diagnosis and confidence."
    )

    st.write(
        "6. Escalate uncertain cases for human review."
    )

    st.divider()

    if st.button("🗑️ Clear Conversation"):

        st.session_state.chat_history = []

        st.rerun()


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    "<div class='hero'>"
    "<h1>🌐 NetForensics AI</h1>"
    "<p class='subtitle'>"
    "Intelligent Network Fault Detection with Responsible AI"
    "</p>"
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# FEATURE CARDS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown(
        "<div class='card'>"
        "<h3>🔍 Smart Detection</h3>"
        "<p>Analyzes Cisco errors, network symptoms and "
        "command outputs to identify possible faults.</p>"
        "</div>",
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        "<div class='card'>"
        "<h3>🧠 Hybrid Intelligence</h3>"
        "<p>Combines rule-based fault detection with "
        "historical case similarity analysis.</p>"
        "</div>",
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        "<div class='card'>"
        "<h3>👨‍💻 Human-in-the-Loop</h3>"
        "<p>Low-confidence diagnoses are flagged for "
        "human expert review and verification.</p>"
        "</div>",
        unsafe_allow_html=True
    )


st.divider()


# ============================================================
# CHATBOT INTRODUCTION
# ============================================================

st.subheader("💬 Network Diagnosis Assistant")

with st.chat_message("assistant"):

    st.write(
        "👋 Hello! I'm NetForensics AI, your intelligent network "
        "troubleshooting assistant. How can I help you today?"
    )


# ============================================================
# CHAT HISTORY
# ============================================================

for chat in st.session_state.chat_history:

    with st.chat_message("user"):

        st.write(chat["question"])


    with st.chat_message("assistant"):

        if chat["type"] == "general":

            st.write(chat["response"])


        elif chat["type"] == "diagnosis":

            st.markdown("## 🚨 Fault Diagnosis")

            st.markdown("### ⚠️ Probable Fault")
            st.success(chat["fault"])

            st.markdown("### 📡 Protocol")
            st.write(chat["protocol"])

            st.markdown("### 🧩 Possible OSI Layer")
            st.write(chat["layer"])

            st.markdown("### 🔎 Root Cause Analysis")
            st.write(chat["reason"])

            st.markdown("### 💻 Verification Command")
            st.code(chat["verification"])

            st.markdown("### 🛠️ Resolution Steps")

            for number, step in enumerate(
                chat["steps"],
                start=1
            ):
                st.write(
                    str(number) + ". " + str(step)
                )

            st.markdown("### ⌨️ Suggested Commands")
            st.code(chat["commands"])

            st.metric(
                "AI Confidence",
                str(chat["confidence"]) + "%"
            )

            st.markdown("### 👨‍💻 Human Review Status")

            if chat.get("human_review_required"):

                if chat["confidence"] >= 50:
                    st.warning(
                        chat["human_review_status"]
                    )
                else:
                    st.error(
                        chat["human_review_status"]
                    )

            else:

                st.success(
                    chat["human_review_status"]
                )

            st.write(
                chat["human_review_message"]
            )

            st.info(
                "Similar Case: "
                + str(chat["similar_case"])
            )


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Ask a question or paste a Cisco Packet Tracer error..."
)


# ============================================================
# PROCESS USER INPUT
# ============================================================

if user_input:

    with st.chat_message("user"):

        st.write(user_input)


    intent = detect_user_intent(user_input)


    # --------------------------------------------------------
    # GREETING
    # --------------------------------------------------------

    if intent == "greeting":

        response_text = (
            "Hello! 👋 Great to have you here. "
            "I'm NetForensics AI, ready to help you analyze "
            "network faults and troubleshoot Cisco network issues."
        )

        with st.chat_message("assistant"):

            st.write(response_text)

        st.session_state.chat_history.append(
            {
                "question": user_input,
                "type": "general",
                "response": response_text
            }
        )


    # --------------------------------------------------------
    # THANK YOU
    # --------------------------------------------------------

    elif intent == "thanks":

        response_text = (
            "You're welcome! 😊 "
            "Whenever you encounter a network fault, "
            "just share the error or symptom with me."
        )

        with st.chat_message("assistant"):

            st.write(response_text)

        st.session_state.chat_history.append(
            {
                "question": user_input,
                "type": "general",
                "response": response_text
            }
        )


    # --------------------------------------------------------
    # GENERAL QUESTION
    # --------------------------------------------------------

    elif intent == "general":

        response_text = (
            "I'm specialized in AI-assisted network fault diagnosis. 🌐\n\n"
            "Share a Cisco Packet Tracer issue, error message, "
            "command output, or network symptom and I can help "
            "identify the probable cause and troubleshooting steps.\n\n"
            "I can assist with VLAN, DHCP, DNS, OSPF, routing, "
            "ARP, ping failures, interface issues and more."
        )

        with st.chat_message("assistant"):

            st.write(response_text)

        st.session_state.chat_history.append(
            {
                "question": user_input,
                "type": "general",
                "response": response_text
            }
        )


    # --------------------------------------------------------
    # NETWORK FAULT DIAGNOSIS
    # --------------------------------------------------------

    elif intent == "diagnosis":

        with st.chat_message("assistant"):

            with st.spinner(
                "🔍 Analyzing network fault..."
            ):

                diagnosis = analyze_fault(user_input)


            confidence = diagnosis["confidence"]

            human_review = get_human_review_status(
                confidence
            )


            st.markdown(
                "## 🚨 Fault Diagnosis Report"
            )


            st.markdown(
                "### ⚠️ Probable Fault"
            )

            st.success(
                diagnosis["fault"]
            )


            st.markdown(
                "### 📡 Protocol / Technology"
            )

            st.write(
                diagnosis["protocol"]
            )


            st.markdown(
                "### 🧩 Possible OSI Layer"
            )

            st.write(
                diagnosis["layer"]
            )


            st.divider()


            st.markdown(
                "### 🔎 Root Cause Analysis"
            )

            st.write(
                diagnosis["reason"]
            )


            st.markdown(
                "### 💻 First Verification Command"
            )

            st.code(
                diagnosis["verification"]
            )


            st.markdown(
                "### 🛠️ Recommended Resolution"
            )

            for number, step in enumerate(
                diagnosis["steps"],
                start=1
            ):

                st.write(
                    str(number) + ". " + str(step)
                )


            commands_text = "\n".join(
                diagnosis["commands"]
            )


            st.markdown(
                "### ⌨️ Suggested Commands"
            )

            st.code(
                commands_text
            )


            st.divider()


            # ------------------------------------------------
            # AI CONFIDENCE
            # ------------------------------------------------

            st.markdown(
                "### 🧠 AI Confidence"
            )

            st.progress(
                int(min(confidence, 100))
            )

            st.write(
                str(confidence) + "%"
            )


            if confidence >= 80:

                st.success(
                    "🟢 High Confidence Diagnosis"
                )

            elif confidence >= 50:

                st.warning(
                    "🟡 Medium Confidence Diagnosis"
                )

            else:

                st.error(
                    "🔴 Low Confidence Diagnosis"
                )


            # ------------------------------------------------
            # HUMAN REVIEW
            # ------------------------------------------------

            st.markdown(
                "### 👨‍💻 Human Review Status"
            )


            if human_review["review_required"]:

                if confidence >= 50:

                    st.warning(
                        human_review["status"]
                    )

                else:

                    st.error(
                        human_review["status"]
                    )

            else:

                st.success(
                    human_review["status"]
                )


            st.write(
                human_review["message"]
            )


            # ------------------------------------------------
            # SIMILAR CASE
            # ------------------------------------------------

            st.markdown(
                "### 📂 Knowledge Base Match"
            )

            st.info(
                "Similar Case: "
                + str(diagnosis["similar_case"])
            )


        # ----------------------------------------------------
        # SAVE DIAGNOSIS TO CHAT HISTORY
        # ----------------------------------------------------

        st.session_state.chat_history.append(
            {
                "question": user_input,
                "type": "diagnosis",
                "fault": diagnosis["fault"],
                "protocol": diagnosis["protocol"],
                "layer": diagnosis["layer"],
                "reason": diagnosis["reason"],
                "verification": diagnosis["verification"],
                "steps": diagnosis["steps"],
                "commands": commands_text,
                "confidence": confidence,
                "similar_case": diagnosis["similar_case"],
                "human_review_status": human_review["status"],
                "human_review_message": human_review["message"],
                "human_review_required": human_review["review_required"]
            }
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🌐 NetForensics AI | AI-Assisted Network Fault Diagnosis "
    "and Responsible Human Review System"
)

