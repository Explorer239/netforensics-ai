### **NetForensics AI: Worked Diagnosis Examples**



###### Purpose



This document contains worked examples demonstrating how NetForensics AI analyzes network fault cases using the structured diagnosis prompt.



Each example provides the network fault input and the expected AI-assisted diagnosis. These examples demonstrate evidence-based troubleshooting, confidence assessment, OSI layer identification, recommended commands, and suggested fix steps.



All AI-generated diagnoses require human review before the suggested fix is accepted or applied.







##### Example 1: VLAN Port Assignment Issue



###### Input Network Fault Case



\*\*Network Topology:\*\*

PC1 → Switch1 → Router1 → Server1



\*\*Protocol or Technology:\*\*

VLAN



\*\*Symptom:\*\*

PC1 cannot reach the default gateway or Server1.



\*\*Evidence:\*\*

`show vlan brief` indicates that the port connected to PC1 is assigned to VLAN 1 instead of the required VLAN 10.

`show interfaces fa0/1 switchport` confirms that FastEthernet0/1 is operating as an access port in VLAN 1.

`ipconfig` shows that PC1 has an IP address configured for the VLAN 10 subnet.







###### AI Diagnosis



\*\*Root Cause:\*\*

PC1 is connected to a switch port assigned to VLAN 1 while its IP configuration belongs to the VLAN 10 network. This VLAN mismatch prevents PC1 from reaching the correct default gateway.



\*\*Confidence:\*\*

High



\*\*Evidence Used:\*\*

The switch port FastEthernet0/1 is assigned to VLAN 1, while PC1 has an IP address belonging to the VLAN 10 subnet.



\*\*OSI Layer:\*\*

Layer 2 – Data Link



\*\*Recommended Next Command:\*\*

`show running-config interface fa0/1`



\*\*Suggested Fix Steps:\*\*



1\. Access the configuration mode of Switch1.

2\. Select interface FastEthernet0/1.

3\. Configure the interface as an access port.

4\. Assign the interface to VLAN 10.

5\. Verify the VLAN assignment using `show vlan brief`.

6\. Test connectivity from PC1 to its default gateway.



\*\*Human Review:\*\*

Required before applying the configuration change.



\---



##### Example 2: Router Interface Down



###### Input Network Fault Case



\*\*Network Topology:\*\*

PC1 → Switch1 → Router1 → Server1



\*\*Protocol or Technology:\*\*

Interface Configuration



\*\*Symptom:\*\*

PC1 cannot ping its default gateway.



\*\*Evidence:\*\*

`show ip interface brief` displays the router interface GigabitEthernet0/0 with the status `administratively down` and protocol status `down`.

`ipconfig` confirms that PC1 has a valid IP address and default gateway configured.







###### AI Diagnosis



\*\*Root Cause:\*\*

The router interface GigabitEthernet0/0 is administratively shutdown, preventing communication between PC1 and its default gateway.



\*\*Confidence:\*\*

High



\*\*Evidence Used:\*\*

The `show ip interface brief` output explicitly indicates that GigabitEthernet0/0 is administratively down.



\*\*OSI Layer:\*\*

Layer 1 – Physical



\*\*Recommended Next Command:\*\*

`show running-config interface gigabitethernet0/0`



\*\*Suggested Fix Steps:\*\*



1\. Access Router1 configuration mode.

2\. Enter the GigabitEthernet0/0 interface.

3\. Enable the interface using the `no shutdown` command.

4\. Verify that the interface status changes to up.

5\. Test connectivity by pinging the default gateway from PC1.



\*\*Human Review:\*\*

Required before applying the configuration change.





##### Example 3: Missing Static Route



###### Input Network Fault Case



\*\*Network Topology:\*\*

PC1 → Switch1 → Router1 → Router2 → Server1



\*\*Protocol or Technology:\*\*

Static Routing



\*\*Symptom:\*\*

PC1 can successfully ping its default gateway but cannot reach Server1 located on a remote network.



\*\*Evidence:\*\*

`show ip route` on Router1 displays directly connected networks but does not contain a route to the Server1 network.

The default gateway ping from PC1 is successful, indicating that local connectivity is working.







###### AI Diagnosis



\*\*Root Cause:\*\*

Router1 does not have a route to the remote network where Server1 is located.



\*\*Confidence:\*\*

High



\*\*Evidence Used:\*\*

The routing table does not contain an entry for the Server1 network, while local gateway connectivity is successful.



\*\*OSI Layer:\*\*

Layer 3 – Network



\*\*Recommended Next Command:\*\*

`show ip route`



\*\*Suggested Fix Steps:\*\*



1\. Identify the destination network address of Server1.

2\. Identify the correct next-hop router address.

3\. Configure a static route toward the remote network.

4\. Verify that the route appears in the routing table.

5\. Test connectivity from PC1 to Server1.



\*\*Human Review:\*\*

Required before configuring the static route.







##### Summary



These worked examples demonstrate the NetForensics AI troubleshooting workflow:



Network Fault Case

↓

Evidence Collection

↓

AI-Assisted Diagnosis

↓

Root Cause Identification

↓

OSI Layer Identification

↓

Next Command Recommendation

↓

Suggested Fix

↓

Human Review

↓

Fix Verification



The examples demonstrate that NetForensics AI provides recommendations based on available evidence and does not automatically apply network configuration changes. A human reviewer must validate every diagnosis before the recommended fix is accepted.



