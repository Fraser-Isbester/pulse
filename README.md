# Pulse
Slack chat interface for Retrievement Augmented Generation (RAG) of knowledge bases.

# Features
- Incoming slack message vectorizer
- slack message responded (:eyes: to trigger a response)

## Inference/Embedding Support
- [x] OpenAI
- [ ] Ollama

## Vector store Support
- [x] Redis
- [x] Postgres
- [ ] Weviate

## Deployment Methods
 - [x] Docker
 - [ ] Kubernetes (Helm)

## Source Loaders
- [x] slack (push)
- [ ] slack (pull)
- [ ] confluence (pull)

# Local Development
- run: `docker compose up --build`
- run: `ngrok http 8000`
- update the request URL to your ngrok url: https://api.slack.com/apps/A06606AF2PR/event-subscriptions?
