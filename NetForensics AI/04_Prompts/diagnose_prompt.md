#### **NetForensics AI: An Intelligent Network Fault Detection and Troubleshooting System**

###### 

##### Diagnosis Prompt Template



###### Purpose



This prompt is used by NetForensics AI to analyze network fault cases and generate an AI-assisted troubleshooting diagnosis.



The AI analyzes the available network topology, protocol or technology, symptoms, and command evidence. The diagnosis is generated based only on the provided information and is later reviewed by a human reviewer.





###### Prompt



You are a network troubleshooting assistant.



Analyze the following network fault case using only the information provided.



Network Topology:

{topology}



Protocol or Technology:

{Category}



Symptom:

{symptom}



Evidence:

{evidence}



Provide the diagnosis in the following format:



Root Cause:



Confidence:



Evidence Used:



OSI Layer:



Recommended Next Command:



Suggested Fix Steps:



Do not make unsupported assumptions.



If the available evidence is insufficient, mention that additional troubleshooting is required.



Human review is mandatory before accepting or applying the suggested fix.





###### Prompt Design Principles



The prompt was designed using the following principles:



1\. \*\*Evidence-Based Diagnosis\*\*

&#x20;  The AI is instructed to use only the information provided in the network fault case.



2\. \*\*No Unsupported Assumptions\*\*

&#x20;  The AI should not invent configuration details or assume faults without evidence.



3\. \*\*Confidence Reporting\*\*

&#x20;  Each diagnosis includes a confidence level to indicate the reliability of the AI recommendation.



4\. \*\*OSI Layer Identification\*\*

&#x20;  The AI identifies the relevant OSI layer associated with the network fault.



5\. \*\*Next Command Recommendation\*\*

&#x20;  The AI suggests an appropriate Cisco troubleshooting command for further investigation.



6\. \*\*Actionable Fix Steps\*\*

&#x20;  The AI provides recommended steps to resolve the identified network issue.



7\. \*\*Mandatory Human Review\*\*

&#x20;  Every AI-generated diagnosis must be reviewed by a human before the fix is accepted or applied.





###### Input Variables



| Variable     | Description                                                |

| ------------ | ---------------------------------------------------------- |

| `{topology}` | Network devices and their connections                      |

| `{protocol}` | Networking protocol or technology related to the case      |

| `{symptom}`  | Observed network problem                                   |

| `{evidence}` | Available show-command output or other diagnostic evidence |





###### Expected Output Fields



| Field                    | Description                              |

| ------------------------ | ---------------------------------------- |

| Root Cause               | Most likely reason for the network fault |

| Confidence               | High, Medium, or Low confidence level    |

| Evidence Used            | Information supporting the diagnosis     |

| OSI Layer                | OSI layer related to the fault           |

| Recommended Next Command | Next command for investigation           |

| Suggested Fix Steps      | Recommended steps to resolve the issue   |





###### Human Oversight



NetForensics AI does not automatically apply configuration changes.



All AI-generated diagnoses are passed to the human review stage, where the reviewer can mark the response as:



\* \*\*Accepted\*\* – The AI diagnosis is correct.

\* \*\*Edited\*\* – The AI diagnosis requires modification.

\* \*\*Rejected\*\* – The AI diagnosis is incorrect.



This human-in-the-loop approach ensures that AI recommendations are validated before being considered final.



