SmartMedID: Secure face biometric Based Medical 
Record Access System 

Pradish G 
School of Computer Science 
Engineering and Information Systems, 
Vellore Institute of Technology, 
Vellore, Tamilnadu, India 
pradish.g2022@vitstudent.ac.in 
________________________________________________________________________________________________________________ 
Abstract

This project, "SmartMedID: Secure Face Biometrics-Based Medical Record Access System", introduces a privacy
focused healthcare solution that integrates facial recognition technology with encrypted patient record management. The system 
employs face biometrics to uniquely identify and authenticate patients, enabling seamless and secure access to their medical 
history. Patient information is encrypted using the Fernet symmetric encryption standard, ensuring data confidentiality, while 
doctor credentials are securely hashed using SHA-256. The platform is built using Python and integrates face detection and 
recognition modules to validate identities before granting access. Each access attempt is logged for accountability. This approach 
enhances hospital efficiency, minimizes unauthorized access, and improves the overall security of digital health records. 
Keywords— Biometrics, Encryption, Electronic Medical records, Secured access, Authentication, Fernet symmetric encryption   
____________________________________________________________________________________________________ 
I. INTRODUCTION 

The rapid digitization of healthcare has transformed how 
patient information is stored, accessed, and managed. 
Traditional paper-based medical records, once the 
standard, are increasingly being replaced by Electronic 
Medical Records (EMRs) due to their efficiency, ease of 
sharing, and potential for integration with advanced 
healthcare technologies. This transformation brings 
significant benefits, including faster retrieval of patient 
histories, 
improved coordination among healthcare 
providers, and the ability to leverage analytics for better 
diagnosis and treatment planning. However, with these 
advantages comes a new set of challenges — data privacy, 
security, and integrity. Medical records contain highly 
sensitive personal information, including a patient’s 
medical history, diagnoses, treatments, medications, and 
sometimes even financial details. Any unauthorized 
access or breach of such data can lead to serious 
consequences, including identity theft, insurance fraud, 
medical malpractice risks, and a loss of patient trust in 
healthcare institutions. The increasing frequency of 
cyberattacks on healthcare organizations worldwide 
highlights the urgent need for robust and secure access 
control mechanisms. 

Traditional authentication methods, such as passwords 
and PINs, have proven insufficient in safeguarding digital 
health records. These methods are prone to common 
vulnerabilities — weak passwords, password sharing, 
phishing attacks, and brute-force hacking. Even smart 
card–based systems, while offering improved security, 
face risks such as theft or duplication. Therefore, 
healthcare systems require a solution that is both highly 
secure and user-friendly, minimizing reliance on 
credentials that can be stolen, guessed, or forgotten. 
Biometric authentication has emerged as a promising 
alternative in this context. Unlike passwords or cards, 
biometrics are based on unique physiological or 
behavioral characteristics of individuals, making them 
much harder to replicate or forge. Among biometric 
modalities, facial recognition stands out due to its non
intrusive nature, high accuracy, and ease of use. Patients 
and healthcare providers can be authenticated simply by 
scanning their faces, eliminating the need for 
remembering codes or carrying additional devices. 
Moreover, facial biometrics can be integrated into existing 
hospital workflows with minimal disruption. 

The SmartMedID: Secure Face Biometrics-Based Medical 
Record Access System builds on this principle, providing 
a 
secure, privacy-focused solution for accessing and 
managing medical records. The system employs face 
detection and recognition modules to uniquely identify 
patients before granting access to their medical history. 
This ensures that only the legitimate patient or authorized 
healthcare personnel can view or update sensitive medical 
data. By implementing Fernet symmetric encryption, the 
system guarantees that patient records remain 
confidential, even if the database is accessed by 
unauthorized parties. 


II. MOTIVATION 

In the modern healthcare environment, security incidents 
are no longer uncommon occurrences — they are costly 
and can destabilize patient confidence. Medical data theft 
incidents point to a more weakness: health systems usually 
use outdated forms of authentication that cannot keep pace 
with contemporary cybersecurity threats. A hijacked 
password or lost smart card can grant an unauthorized user 
XXX-X-XXXX-XXXX-X/XX/$XX.00 ©20XX IEEE 
complete access to a patient's confidential health record, 
with both individual and systemic effects. 
While hospitals work to implement more secured 
electronic medical record systems, the integration of access 
and security continues to be a difficult balance to meet. 
Physicians need immediate access to patient histories in 
life-threatening situations, but security measures must 
guarantee that this access is given only to the authorized 
individual. The problem of how to make quick secured 
access available without inviting an intruder — is the 
central issue that prompted this project. 
Facial biometrics provides a good chance to end this 
problem. An individual's face is both inherently unique and 
immediately verifiable, so access can be secure without 
passwords or additional devices. Each and every design 
choice — from Fernet encryption of patient data to SHA
256 hashing of physician credentials — is driven by the 
impulse to restrict the unauthorized access, enhance 
hospital productivity, and regain patient trust in health 
systems. 


III. PROPOSED METHODOLOGY 

The SmartMedID system methodology being proposed 
would combine facial recognition technology with 
advanced encryption methods to grant safe access to 
electronic medical records. It starts off with capturing 
real-time facial images, which are then preprocessed and 
their features extracted via face detection and recognition 
modules coded using Python. The facial features captured 
are then compared with biometric templates stored to 
verify patients or enrolled doctors. Upon authentication, 
the 
system provides access to encrypted medical 
information, whereby patient data is safeguarded using 
Fernet symmetric encryption standard and doctor 
credentials are hashed securely using SHA-256 hashing. 
All attempts at access, both valid and invalid, are logged 
securely for auditing and accountability. This modular 
Python-based architecture maintains data confidentiality, 
prohibits unauthorized access, and allows for easy 
integration into hospital processes to improve security as 
well as operational effectiveness. 


IV. LITERATURE SURVEY 

This paper presents a new encryption scheme that is 
specially for protecting facial images to be used in 
biometric verification systems. The technique addresses 
tamper attacks on facial image databases by making stored 
images tamper-proof. The algorithm utilizes the 2D 
Hénon chaotic map to shuffle pixels (permutation) and 
further substitutes them with Class-III one-dimensional 
cellular automata rules (Rule 90). The technique proposed 
provides a huge key space and shows resistance against 
statistical attacks. Experimental tests—such as histogram 
entropy, correlation coefficients, and NIST tests—result in 
low pixel correlation and high information entropy, 
validating its efficacy for use in securing biometric 
systems.[1] 

This paper, read at the 5th International Conference on 
Electronics and Sustainable Communication Systems 
(ICESC 2024), brings forward Med Vault, a biometric 
system intended for protecting and maintaining patient 
medical records. The system employs biometric 
authorization—most probably fingerprint or the like—to 
maintain secure access to patients' data based on 
distinctive identifiers. It streamlines retrieval of the 
records and secures the data by making access dependent 
on biometric entry. Implementation details specify the 
system architecture and healthcare workflow integration. 
Initial 
deployment indicates enhanced safety and 
simplified access control, with scalability and privacy 
likely future enhancements.[2] 

This paper proposes a lightweight biometric-based user 
authentication system intended for healthcare settings. It 
protects electronic health records (EHR) sent over 
possibly insecure wireless links, in such a way that only 
users with proper authority are able to access them. The 
system employs temporary local identifiers instead of 
global user IDs in order to maintain privacy, yet permit 
global ID recovery in critical situations. It also uses a data 
access control mechanism that allows users to access data 
strictly based on their privileges. The scheme is verified 
through both formal and informal security analyses and a 
performance evaluation, proving its feasibility for secure 
healthcare applications.[3] 

In this chapter, Raposo discusses the increasing use of 
facial recognition (FR) technologies in healthcare—
 variously from tracking emotions and health risk to 
disease diagnosis and patient identification—emphasizing 
its usefulness as well as danger. The chapter highlights the 
legal 
and ethical risks of FR, including bias, 
discrimination, and misoutputs that can jeopardize patient 
rights and service quality. It specifically highlights the 
regulative intricacy in the European Union where FR 
comes under overlapping regulations such as the General 
Data Protection Regulation (GDPR), the Medical Devices 
Regulation, and the upcoming AI Regulation, which 
complicate compliance for healthcare professionals. It 
contends that this cross-linking of regulations can deter 
stakeholders from using FR despite its constructive 
advantage. [4] 

This research addresses the hygiene issues of conventional 
registration processes (such as ID cards or fingerprint 
readers) exacerbated by the COVID-19 pandemic. The 
Contactless Registration system presented leverages facial 
recognition to verify patients at registration: if a face 
matches a stored record in a database, the patient's records 
are accessed; else, a new registration is made. It is 
validated on a bespoke dataset with a success rate of about 
94%. Its performance is, however, significantly impaired 
in 
makeup cases, suggesting facial alteration 
sensitivity.[5] 

This book chapter presents a technological model making 
use of facial recognition to reliably identify patients in 
medical environments and avoid medical identity theft. 
The system was deployed as a proof of concept at the 
UROGINEC clinic, providing successful patient 
identifications with an average precision of 95.82% and 
response times of approximately 3 seconds. The fast and 
accurate matching provided added security and better user 
experience while registering and verifying patients. The 
model efficiently raised warnings against impersonation 
threats, thus enhancing patient safety protocols within the 
institution [6] 

This article describes an identity-based biometric 
encryption testbed implementation to provide security for 
Internet of Medical Things (IoMT) data communication in 
medical environments. It utilizes facial biometric 
characteristics of clinicians as identity-based public keys 
to encrypt patients' vital information, which can be 
securely transmitted through IoMT devices such as 
ESP32. The system utilizes an edge device (Jetson Nano) 
for decryption and biometric authentication utilizing 
Fuzzy Identity-Based Encryption (FIBE), followed by 
secure uploading of the data onto a cloud platform 
(ThingsBoard). A deep learning–based Intrusion 
Detection System (IDS) is used to safeguard data in the 
cloud against malicious attacks. The testbed features a 
privacy-preserving, real-time solution for securing 
sensitive healthcare data in IoMT environments [7] 

This conference paper proposes a multi-biometric 
recognition model applicable to e-healthcare uses, relying 
on the use of image analysis methods for strengthening 
patient verification and system security. While the full 
methodology is not available to the public, the research 
was published at the 2023 International Conference on 
Advancement in Computation & Computer Technologies 
(InCACCT) and deals with the integration of multiple 
biometric modalities in healthcare systems. The emphasis 
is on enhancing patient identification accuracy with 
combined biometric data analysis in digital healthcare 
settings.[8] 

This paper suggests an Emergency Medical Access 
Control System on a public blockchain to facilitate secure 
and worldwide sharing of patient Electronic Health 
Records (EHRs) in emergencies. Compared with earlier 
permissioned blockchain solutions, it enables any 
emergency physician to access required medical 
information without prior registration, even when the 
patient is abroad and unconscious. The system uses a 
tamper-resistant pendant with biometric verification, 
carried by the patient, to authenticate and initiate secure 
data exchange. The family physician encrypts the EHR, 
places it in IPFS, and employs smart contracts for access. 
Emergency physicians authenticate through the pendant, 
execute a Diffie-Hellman (DH) key exchange, and get 
decryption keys over a secure channel. Ethereum's Sepolia 
testnet was tested, and the process was found to be low
cost and convenient, and it had inbuilt security against 
intrusions.[9] 

This paper introduces an iris-based cancelable biometric 
cryptosystem for securely storing patients' health 
information on smart cards. It combines cancelable 
biometrics with a fuzzy commitment scheme and Reed
Solomon coding to securely associate a symmetric 
encryption key with a modified iris template, without ever 
storing or recalling the key. The encrypted information, 
the helper data, and a cryptographic hash of the key are on 
the card, but the key is rebuilt on-the-fly during the 
authentication process. With AES encryption and SHA
512 hashing, the system has a maximum 252-bit key 
length with 0% FAR and 7% FRR. Security analysis 
provides resistance against stolen card attack, cross
matching, masquerading, brute force, and record 
multiplicity attacks, both for authentication and data 
privacy.[10] 

This paper presents a thorough overview of privacy 
threats, attacks, and defense methods pertaining to 
biometric-based smart healthcare systems. The paper 
identifies how biometric information—being permanent, 
unique, and un-revocable—provides robust authentication 
but induces drastic privacy threats if leaked. The paper 
classifies attacks like spoofing, replay attacks, cross
matching, template inversion, and adversarial ML attacks, 
and discusses their implications for healthcare data 
security. It also elaborates on privacy-preserving methods 
such as biometric template protection, homomorphic 
encryption, cancelable biometrics, and secure multiparty 
computation. Particular focus is put on striking a balance 
between usability, precision, and security while being in 
line with healthcare privacy mandates. The review 
outlines open research issues such as computational 
efficiency, immunity to cutting-edge AI-based attacks, 
and 
interoperability 
platforms.[11] 

across 
various 
healthcare 
The paper suggests Patient Medical Record Monitoring 
System, which combines IoT-based biometric hardware 
with blockchain technology to provide secure, transparent, 
and real-time health monitoring. The system employs 
wearable equipment like smartwatches, digital face masks, 
smart gloves, and goggles to take patients' vital signs and 
biometric identifiers. Information is preserved on both 
hospital and government databases, associated with 
Aadhaar-based authentication, and locked on the 
Ethereum blockchain with smart contracts. The design 
supports remote tracking, real-time detection of outliers, 
and integration with AI/ML for predictive health 
analytics. Blockchain provides immutability, privacy, and 
access control, whereas the cloud facilitates worldwide 
availability of data. Despite the promise of enhanced 
diagnosis, lower rates of medical error, and enhanced 
planning for healthcare facilities, the system is hampered 
by high costs, technical sophistication, and low uptake in 
rural locations.[12] 

This essay examines the application of biometric 
technology in protecting electronic health records (EHRs) 
in shared care settings, where various healthcare 
professionals have access to confidential patient data. It 
contrasts biometrics with conventional verification 
techniques such as passwords, PINs, and smart cards and 
offers benefits such as enhanced security, impersonation 
prevention, lower maintenance expenses, and remote 
access suitability. The research identifies several 
biometric uses, such as authentication, access control, 
medical data encryption, secure data exchange, 
verification of patient identity, and fraud detection. It 
addresses challenges such as usability problems, 
limitations of accuracy, environmental influences, and 
integration expenses, pointing out that although 
biometrics present enormous security advantages over 
conventional 
methods, technical and operational 
impediments still exist. The authors summarize that 
biometrics can improve privacy, confidentiality, and data 
protection in health care but additional effort must be 
made to overcome implementation challenges and 
maximize use in varied medical environments.[13] 

This article discusses a brief overview of biometric 
technologies and their potential usage in improving 
security in several areas, mostly in authentication and 
identity management. It describes various biometric 
modalities, including fingerprint, iris, face, voice, and 
signature recognition, and contrasts them based on 
accuracy, reliability, and appropriateness for a particular 
use case. The report points out benefits of using 
biometrics in place of conventional methods of 
authentication, with greater security, convenience, and 
protection against impersonation. It further discusses real
world usage of biometrics in access control, border 
control, and financial transactions and technical and 
operational challenges such as environmental impact, 
system integration, cost, and user acceptance. The paper 
concludes that though biometrics present a promising 
solution for user-friendly and secure authentication, 
effective 
implementation 
relies 
on overcoming 
performance constraints and privacy protection.[14] 

This paper discusses the application of biometric 
authentication as a safe means of identity verification in 
computer systems, highlighting its superiority over 
standard password- or token-based methods. It explains 
different biometric modalities, including fingerprint, iris, 
and face recognition, and how they can be utilized to 
protect sensitive information and systems. The research 
highlights the uniqueness and consistency of biometric 
features, making them more resistant to theft or 
replication, while pointing out issues such as variations in 
accuracy based on environmental conditions, aging, or 
system failure. Practical application examples are 
discussed, showing how biometrics can be applied for 
access control, secure transactions, and identification. The 
report concludes that biometrics, when paired with good 
encryption and sound system design, has the potential to 
greatly improve security, but needs to be implemented 
with thoughtful regard for privacy, usability, and 
integration issues.[15] 

This essay explains the importance of biometric 
authentication for improving information system security, 
its superiority over traditional methods like passwords, 
PINs, and access cards, and discusses different biometric 
methods like fingerprint, iris, face, and voice recognition 
and compares them on accuracy, reliability, and 
applicability grounds. The research focuses on the 
increasing use of biometrics in industry areas such as 
banking, border control, and healthcare due to their 
capability 
to 
offer 
uncopyable, 
one-of-a-kind 
identification. The research also looks into challenges of 
implementation such as environmental factors, cost of 
systems, privacy, and user acceptance. The paper 
concludes that although biometrics offer a very secure and 
easy-to-use authentication method, consideration of 
technological factors and ethics is crucial for efficient 
implementation.[16] 

This paper discusses the implementation of biometric 
authentication in healthcare systems to secure and protect 
electronic medical records. It presents the weaknesses of 
conventional authentication tools like passwords and 
smart cards, which can be stolen, lost, and shared without 
authorization. The research indicates the benefits of 
biometrics, especially fingerprint and face recognition, in 
offering exclusive, non-reproducible identification for 
patients and health practitioners alike. It addresses system 
design issues, such as encryption of medical records, 
storage of biometric templates in a secure manner, and 
adherence to data protection laws such as HIPAA. 
Challenging implementation such as cost, environmental 
issues, and acceptability by users are also elaborated upon. 
The conclusion reached by the paper is that biometric
based healthcare systems can effectively prevent 
unauthorized access, enhance efficiency of operations, and 
enhance patient trust, as long as technical and ethical 
issues are well addressed.[17]

This essay examines the application of facial recognition 
technology as a secure, effective means for authentication 
across different fields with emphasis on privacy protection 
and barring unauthorized access. It outlines the operation 
modes of facial recognition, such as image capture, 
feature extraction, and pattern matching, and contrasts its 
performance with other biometric techniques. The work 
highlights the benefits of facial recognition, including 
non-intrusiveness, efficiency, and appropriateness for 
remote verification, and notes challenges such as 
variations in lighting, differences in pose, and spoofing 
attacks. Real-world usage for security systems, border 
control, and healthcare is considered, with integration 
examples for encryption methods to secure stored 
biometric data. The research concludes that face 
recognition, when paired with strong security controls, 
can become an effective and convenient authentication 
solution as long as accuracy and privacy issues are 
resolved.[18] 

This paper proposes a system to secure medical records by 
using a private blockchain combined with advanced deep 
encryption and the SHA-256 algorithm. The methodology 
is designed to create a secure, transparent, and efficient 
data ecosystem by giving patients control over their 
records, enhancing data integrity, and improving 
interoperability between different healthcare systems. 
While the proposed system demonstrates a higher 
accuracy rate of 88% compared to existing systems, the 
paper acknowledges challenges such as the vulnerability 
of current centralized systems, scalability and regulatory 
issues with blockchain implementation, and the need to 
address strict ethical and legal requirements for patient 
privacy.[19] 

This paper, titled "Securing electronics healthcare records 
in Healthcare 4.0: A biometric-based approach," proposes 
a new biometric-based authentication scheme to secure 
access to electronic health records (EHR) stored on a 
cloud server. The methodology uses elliptic curve 
cryptography (ECC) and biometric templates to generate a 
secure key pair, which is then validated using the 
AVISPA tool. The system connects wearable devices, 
mobile devices, and a cloud server to manage and store 
patient data securely. The paper's findings indicate that the 
proposed scheme has a lower computational and 
communication cost than existing methods and is resistant 
to various cyberattacks, thereby ensuring the security and 
integrity of patient data.[20] 

 
S.no. Paper Title Methodology used Advantages Disadvantages 


1 An Efficient and 
Robust Facial Image 
Encryption Algorithm 
for Biometric Identity 
Systems   
Hénon map, Class-III 
1D Cellular Automata, 
Security analyses 
Low correlation between 
adjacent pixels  
Potential computational overhead 
during encryption/decryption 

2 Design and 
Implementation of 
Med Vault – 
Biometric-based 
Medical Record 
System   
Fingerprint recognition Enhances security with 
biometric-based authentication 
Implementation may require 
additional hardware and cost 

3 Secure and Privacy 
preserving Biometric 
based User 
Authentication with 
Data Access Control 
System in the 
Healthcare 
Environment 
Biometric authentication Protects sensitive healthcare 
data transmitted over wireless 
networks 
Full methodology and performance 
metrics aren't publicly accessible 
without full text 

4 Facial recognition AI 
technology in 
healthcare and the law 
Facial recognition for 
emotion analysis 
Improves patient identification 
accuracy 
Risk of erroneous, biased or 
discriminatory outcomes 
5 Contactless Patient 
Authentication for 
Registration Using 
Face Recognition 
Technology 
Face recognition 
(biometric) for touchless 
authentication 
Hygienic and touch-free 
registration—particularly 
valuable during pandemics 
Reduced accuracy in cases with 
makeup or facial alterations 

6 Technological Model 
of Facial Recognition 
for the Identification 
of Patients in the 
Health Sector 
Facial recognition 
system integrated into 
clinic operations 
Reduces medical identity theft 
via alerts 
Details on false rejection/acceptance 
rates not provided 

7 A Testbed 
Implementation of a 
Biometric Identity
Based Encryption for 
IoMT-enabled 
Healthcare System    
Fuzzy Identity-Based 
Encryption (FIBE) using 
clinicians’ facial 
biometrics, Deep 
learning–based Intrusion 
Detection System (IDS)                 
Supports real-time, privacy
aware transmission of patient 
vitals 
Reliance on clinician biometrics; fail 
safes for biometric capture issues not 
discussed 

8 Image Analysis for E
Healthcare Systems 
using Multi-Biometric 
Recognition Model 
Multi-biometric 
recognition model 
Enhances authentication 
accuracy through multi-modal 
biometric input 
Unspecified biometric modalities 
and performance metrics 

9 Emergency Medical 
Access Control 
System Based on 
Public Blockchain 
Diffie-Hellman (DH) 
key exchange protocol 
Low operational cost Risk of pendant theft, though 
mitigated by biometric 
authentication. 

10 Iris Based Cancelable 
Biometric 
Cryptosystem for 
Secure 
Healthcare Smart Card 
AES encryption, SHA
512 hashing 
High key length (252 bits) 
suitable for modern 
cryptography. 
FRR of 7% may reject legitimate 
users. 

11 Privacy and 
Biometrics for Smart 
Healthcare Systems: 
Attacks 
and Techniques 
Biometric authentication 
(various modalities) 
Strengthens authentication and 
identity verification. 
Computational overhead in advanced 
encryption methods. 
12 Patients Medical 
Record Monitoring 
Using IoT Based 
Biometrics 
Blockchain 
Security System 
IoT wearable sensors 
(smartwatch, digital face 
mask, smart gloves, 
goggles) 
Real-time patient monitoring 
with anomaly alerts 
Dependence on reliable power and 
internet 

13 Biometrics for 
Electronic Health 
Records 
Biometric authentication 
technologies versus 
traditional methods 
(passwords, PINs, smart 
cards) 
Stronger security than 
traditional methods—biometric 
traits cannot be lost, stolen, or 
easily forged. 
Not always tested for large-scale 
shared care environments.

14 Retracted: Biometric 
Authentication for 
Intelligent and Privacy 
Preserving 
Healthcare Systems 
Empirical methodology  Biometric keys are impossible 
to steal or forget. 
There are potential barriers in data 
collection, storage, and the 
possibility of system crashes or 
authentication problems. 

15 Securitizing Patient 
Record and Access 
Using 
Ethereum Smart 
Contract Graph 
Embedded 
Pyramid Network 
Face Recognition 
Ethereum Smart 
Contract Graph 
Embedded and Pyramid 
Network (ESCGE-PN) 
The proposed ESCGE-PN 
method achieved higher 
performance compared to other 
methods. 
Some prior work failed to address 
data confidentiality and integrity.

16 Privacy-aware smart 
card based biometric 
authentication scheme 
for e-health 
Privacy-aware smart 
card based biometric 
authentication (PSBA) 
scheme 
It requires only half the 
number of parameters to be 
calculated compared to the 
previous scheme 
It fails to provide user anonymity. 

17 A Secure Face 
Recognition for IoT
Enabled Healthcare 
System 
FaceCrypto System Protects against various 
software, network, channel, 
and database attacks. 
Existing IoT systems face serious 
security and privacy issues, such as 
database and channel attacks.

18 Secure and efficient 
privacy protection 
system for medical 
records 
Biohashing Combines the strengths of both 
spatial and frequency domains, 
ensuring strong robustness 
There are many shortcomings 
associated with the sole use of these 
methods. 

19 Securing medical 
records with privacy
preserving storage in 
the cloud through 
advanced deep 
encryption 
SHA-256 Encryption 
and Hash Generation 
Patients have command over 
who can access their health 
information and can grant or 
revoke access. 
The medical industry has strict 
ethical and legal requirements to 
protect patient privacy. 

20 Securing electronics 
healthcare records in 
Healthcare 4.0: A 
biometric-based 
approach 
Biometric authentication The system offers a secure way 
to access electronic health 
records from a cloud server. - 

 
V. RESEARCH GAPS 
Existing studies often lack robust integration of biometric 
authentication with end-to-end encryption that complies 
with healthcare data protection regulations such as 
HIPAA and GDPR. Many systems are still vulnerable to 
spoofing attacks, with limited deployment of advanced 
liveness detection methods suitable for clinical settings. 
Real-world adaptability is also underexplored, as most 
evaluations are conducted in controlled environments 
rather than in hospitals where factors like poor lighting, 
patient movement, and mask usage can affect accuracy. 
Moreover, interoperability with existing Electronic Health 
Record (EHR) platforms and scalability across large 
healthcare networks are rarely demonstrated. The 
potential of multi-modal biometric fusion (e.g., combining 
face, iris, and voice recognition) to improve accuracy and 
resilience is underutilized. Finally, there is a scarcity of 
research on patient acceptance, ethical implications, and 
secure deployment in low-resource or offline healthcare 
environments, leaving significant room for improvement 
in both technological and societal dimensions. 


VI. CONCLUSION 

As a conclusion, the SmartMedID: Secure Face 
Biometrics-Based Medical Record Access System 
provides a powerful, privacy-based solution to the 
challenge of securing electronic medical records by 
incorporating facial recognition technology, encryption, 
and secure credential management. Through the use of 
Fernet symmetric encryption for patient information, 
SHA-256 hashing for credentials of doctors, and a logging 
system for transparency, the system ensures both data 
confidentiality 
and operational transparency. 

The incorporated python modular architecture allows for non
disruptive integration into healthcare processes, enhancing 
productivity without compromising the high standards of 
security. This methodology not only reduces unauthorized 
access but also increases patient trust, leading the way 
towards safer and more efficient electronic healthcare 
environments. 


VII. FUTURE WORK 

In the future, the SmartMedID system may be further 
improved by incorporating multi-factor authentication that 
can fuse facial recognition with other security layers like 
fingerprint identification, voice verification, or OTPs for 
important operations. This will further enhance access 
control as well as reduce the risk in high-security 
healthcare environments. The system can further be 
extended to include cloud-based storage with end-to-end 
encryption, allowing secure and scalable access to patient 
records in several hospital branches or remote 
consultation installations. 

In addition, more advanced deep learning algorithms can 
be used to enhance face recognition accuracy in adverse 
situations like low light, partial occlusion, or aging of 
patients with time. In collaboration with hospital 
information systems, telemedicine software, and wearable 
health sensors may offer physicians real-time patient 
health information for better clinical decision-making. In 
addition, the system may incorporate anomaly detection 
rules to detect abnormal login patterns, triggering 
administrators automatically about potential security 
violations. 


REFERENCES 

[1] Kumar, R., & Santhanavijayan, A. (2023, November). 
An Efficient and Robust Facial Image Encryption 
Algorithm for Biometric Identity Systems. In 2023 
International Conference on Computing, Communication, 
and Intelligent Systems (ICCCIS) (pp. 249-254). IEEE. 

[2] Srinivasan, D., Karthikeyan, S., Sivasanjeev, R., & 
Srimathi, M. (2024, August). Design and Implementation 
of Med Vault-Biometric-based Medical Record System. 
In 2024 5th International Conference on Electronics and 
Sustainable Communication Systems (ICESC) (pp. 1874
1877). IEEE. 

[3] Kaul, S. D., Murty, V. K., & Hatzinakos, D. (2020, 
September). Secure and privacy preserving biometric 
based user authentication with data access control system 
in the healthcare environment. In 2020 International 
Conference on Cyberworlds (CW) (pp. 249-256). IEEE. 

[4] Raposo, V. L. (2024). Facial recognition AI 
technology in healthcare and the law. Research Handbook 
on Health, AI and the Law, 41-56. 

[5] Tay, K. Y., Pang, Y. H., Ooi, S. Y., & Goh, F. L. 
(2021). 
Contactless 
Patient 
Authentication 
for 
Registration Using Face Recognition Technology. In 
Computational Science and Technology: 7th ICCST 2020, 
Pattaya, Thailand, 29–30 August, 2020 (pp. 71-80). 
Singapore: Springer Singapore. 

[6] La Madrid, D., Barriga, M., & Shiguihara, P. (2018, 
October). Technological model of facial recognition for 
the identification of patients in the health sector. In 
Brazilian Technology Symposium (pp. 595-603). Cham: 
Springer International Publishing. 

[7] Aggarwal, M., Zubair, M., Unal, D., Al-Ali, A., 
Reimann, T., & Alinier, G. (2021, December). A testbed 
implementation of a biometric identity-based encryption 
for IoMT-enabled healthcare system. In Proceedings of 
the 5th International Conference on Future Networks and 
Distributed Systems (pp. 58-63). 

[8] Bansal, N., Arora, P., Sharma, D. K., Gupta, K. D., & 
Kuntala, C. (2023, May). Image Analysis for E
Healthcare Systems using Multi-Biometric Recognition 
Model. In 2023 International Conference on Advancement 
in Computation & Computer Technologies (InCACCT) 
(pp. 639-644). IEEE. 

[9] Takahashi, T., Zhihao, Y., & Omote, K. (2024). 
Emergency Medical Access Control System Based on 
Public Blockchain. Journal of Medical Systems, 48(1), 90. 

[10] Kausar, F. (2021). Iris based cancelable biometric 
cryptosystem for secure healthcare smart card. Egyptian 
Informatics Journal, 22(4), 447-453.

[11] Wells, A., & Usman, A. B. (2024). Privacy and 
biometrics for smart healthcare systems: attacks, and 
techniques. Information Security Journal: A Global 
Perspective, 33(3), 307-331. 

[12] Gautam, K. K., Prakash, S., & Dwivedi, R. K. (2023, 
June). Patients medical record monitoring using IoT based 
biometrics 
blockchain security system. In 2023 
International Conference on IoT, Communication and 
Automation Technology (ICICAT) (pp. 1-6). IEEE. 

[13]Flores Zuniga, A. E., Win, K. T., & Susilo, W. (2010). 
Biometrics for electronic health records. Journal of 
medical systems, 34(5), 975-983. 

[14]Healthcare Engineering, J. O. (2023). Retracted: 
Biometric Authentication for Intelligent and Privacy
Preserving Healthcare Systems. 

[15]Gayathri, D., & Raghavcndran, V. (2024, December). 
Securitizing Patient Record and Access Using Ethereum 
Smart Contract Graph Embedded Pyramid Network Face 
Recognition. In 2024 13th International Conference on 
System Modeling & Advancement in Research Trends 
(SMART) (pp. 166-176). IEEE. 

[16] Chen, L., & Zhang, K. (2021). Privacy-aware smart 
card based biometric authentication scheme for e-health. 
Peer-to-Peer Networking and Applications, 14(3), 1353
1365. 

[17] Sardar, A., Umer, S., Rout, R. K., Wang, S. H., & 
Tanveer, M. (2023). A secure face recognition for IoT
enabled healthcare system. ACM Transactions on Sensor 
Networks, 19(3), 1-23. 

[18] Ramzan, M., Habib, M., & Khan, S. A. (2022). Secure 
and efficient privacy protection system for medical 
records. Sustainable Computing: Informatics and Systems, 
35, 100717. 

[19] Sangeetha, M., Aakash, K., Dharun, M., & 
Mohammed Bilal, S. S. (2024, March). Securing Medical 
Records with Privacy-Preserving Storage In the Cloud 
Through Advanced Deep Encryption. In 2024 2nd 
International Conference on Artificial Intelligence and 
Machine Learning Applications Theme: Healthcare and 
Internet of Things (AIMLA) (pp. 1-5). IEEE. 

[20] Haleem, A., Javaid, M., Singh, R. P., & Suman, R. 
(2022). Medical 4.0 technologies for healthcare: Features, 
capabilities, and applications. Internet of Things and 
Cyber-Physical Systems, 2, 12-30. 
