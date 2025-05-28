# InboxMemory AI

> **📁 For detailed setup and development instructions, please check the respective READMEs inside the [`backend/`](./backend/) and [`frontend/`](./frontend/) folders.**

## Postmark Hackathon Project

This project was built for the **Postmark Challenge: Inbox Innovators** hackathon.

🔗 **Blog Post**: [Read more about this project](https://dev.to/ashiqsultan/inboxmemory-ai-rag-your-emails-postmark-1l63)

## What is InboxMemory AI?

[![InboxMemory AI Demo](https://img.youtube.com/vi/XntMQ-oCOQ4/0.jpg)](https://www.youtube.com/watch?v=XntMQ-oCOQ4)


InboxMemory AI is like **ChatGPT for your emails**. It's an intelligent email assistant that transforms your inbox into a searchable knowledge base using RAG (Retrieval Augmented Generation) technology.

### Key Features

- **📧 Email-to-Knowledge**: Forward emails to create a searchable knowledge base
- **🤖 Natural Language Q&A**: Ask questions about your emails in plain English
- **✉️ Email Interface**: Query via email or through the web app
- **🔍 Smart Search**: AI-powered semantic search through your email content
- **⚡ Quick Setup**: Just send "Hi [your name]" to `ai@kbhelper.com` to get started

### How It Works

1. **Store**: Forward emails to build your knowledge base - emails are chunked and stored in a vector database
2. **Query**: Ask questions via email or the web app
3. **Get Answers**: AI searches through your saved content and provides intelligent responses

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL for email storage
- **Vector Database**: LanceDB for semantic search
- **Cache & Rate Limiting**: Redis
- **Frontend**: React
- **AI**: Google Gemini for embeddings and natural language processing
- **Deployment**: Docker
- **Email Service**: Postmark

## Getting Started

### Quick Start (Email Interface)
Send "Hi [your name]" to **`ai@kbhelper.com`** - the AI will pick up your name, create your account, and you're ready to go! ⚡

### Development Setup
Check the individual README files in the `backend/` and `frontend/` folders for detailed setup instructions.
- **QA via Email**: Forward emails to build knowledge base, then ask questions via email
- **QA via Web App**: Use the React frontend for a more interactive experience
- **Smart Retrieval**: Get contextual answers from your email archive


