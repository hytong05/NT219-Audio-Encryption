**ENCRYPTION OF AUDIO DATA ON A MULTIMEDIA PRODUCT SERVICE PLATFORM**

**Student:** Duong Pham Huy Thong
**Student ID Number:** 2252121431
**Student:** Cao Qui
**Student ID Number:** 22521208
**Class:** NT219.O11.ANTN
**University of Information Technology**
**Lecturer:** PhD. Nguyen Ngoc Tu

Ho Chi Minh City, January 2024

---

## Table of Contents

1. Introduction
2. Background
3. Proposed Solution and Implementation
4. Experiments and Results
5. Conclusion and Future Work

---

## 1. Introduction

### 1.1. Project Topic

* **Title:** Audio Data Encryption on a Multimedia Product Service Platform

### 1.2. Problem Context

* The volume of audio data is rapidly increasing, encompassing films, videos, podcasts, online music, etc.
* Multimedia service platforms require robust encryption solutions to store, transmit, and secure audio data effectively.
* Enhancing the encryption of audio data improves user experience on mobile and internet-connected devices.

### 1.3. Motivation

* Audio is a crucial component of multimedia services. Encrypting audio data ensures that users can access high-quality and seamless audio on the platform.
* Audio encryption provides a security mechanism to prevent unauthorized access and tampering during transmission.

### 1.4. Objectives

* Develop an encryption and decryption system that guarantees the confidentiality, integrity, and availability of audio when streamed.

### 1.5. Stakeholders

* **Service Provider:** Implements security measures, provides encryption mechanisms, and ensures quality of service.
* **Author:** Uploads music/audio files.
* **User:** Registers, logs in, purchases content, and streams audio.
* **Infrastructure:** Provides a secure and stable environment for storage and transmission.
* **Attacker:** Attempts unauthorized access to copyrighted content.

### 1.6. Proposed Solution

* Build an online music streaming platform.
* Encrypt and securely store audio data.
* Decrypt and serve audio data to authorized users.

---

## 2. Background

### 2.1. Double DNA Encoding

* A dual-stage encoding process using DNA-based addition.
* Binary data is mapped to DNA sequences (A, C, G, T) following specific encoding rules.
* DNA addition is applied between the binary data sequence and two other DNA sequences.
* The result is re-converted to binary format for the next encryption steps.

### 2.2. Chaotic Maps

* Chaotic maps generate high-entropy pseudo-random sequences.
* They provide non-linearity and sensitivity to initial conditions, essential for robust encryption.
* We utilize two types: Sine-Cosine Map (SC map) and Logistic Sine-Cosine Map (LSC map) to improve randomness and overcome limitations of traditional maps.

---

## 3. Proposed Solution and Implementation

### 3.1. System Architecture

* The author uploads an audio file.
* The system encrypts the file, generates a one-time use key, and stores the encrypted file and key in the database.
* The user logs in and selects a song.
* The system fetches the encrypted audio and decrypts it using the one-time key.
* The VLC media player interface streams the audio to the user.

### 3.2. Encryption Process

* Import and store audio data.
* Initialize encryption key and vector.
* Generate pseudo-random sequence using chaotic maps.
* Perform permutation and diffusion.
* Generate SecretKey and InitialVector.
* Encrypt the audio data.

### 3.3. Decryption Process

* Import the encrypted audio file.
* Initialize decryption parameters.
* Reproduce pseudo-random sequence using chaotic maps.
* Reverse permutation and diffusion.
* Decrypt the audio data.

---

## 4. Experiments and Results

* Secure user registration and login, with hashed password storage.
* Users select audio; encryption and decryption processes are triggered.
* A one-time use key is generated and tracked in the database.
* The decrypted audio is streamed via VLC; temporary decrypted files are automatically deleted after playback.

---

## 5. Conclusion and Future Work

### 5.1. Conclusion

* Successfully developed a basic platform for secure online audio streaming.
* Achieved successful encryption and decryption with expected performance metrics.
* Ensured data confidentiality and prevented unauthorized access.

### 5.2. Future Work

* Explore new encryption algorithms (e.g., lossless encryption, feature-based encryption, and voice recognition).
* Extend support for multiple audio formats (mp3, wav, m4a).
* Integrate with popular platforms (YouTube, Spotify, SoundCloud).
* Develop online and mobile-based audio encryption solutions.
* Expand to a full online system with additional services.
* Optimize encryption algorithms for better real-time performance.
