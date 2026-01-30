// Placeholder for future enhancements (analytics, auth, or form handling).
// Intentionally minimal for a static GitHub Pages deployment.

// --- Local Chat Demo (Phase 2 UI) ---
// This section wires the homepage chat UI to the FastAPI backend.
// It is designed to be modular so we can add auth, payments, or persistence later.

(() => {
	const chatLog = document.getElementById("chatLog");
	const chatInput = document.getElementById("chatQuestion");
	const chatSubmit = document.getElementById("chatSubmit");
	const chatStatus = document.getElementById("chatStatus");

	// If the chat UI is not on this page, do nothing.
	if (!chatLog || !chatInput || !chatSubmit || !chatStatus) {
		return;
	}

	// In-memory conversation log (per page load).
	const conversation = [];

	const setStatus = (message) => {
		chatStatus.textContent = message || "";
	};

	const appendMessage = (role, text) => {
		const message = document.createElement("div");
		message.className = `chat-message ${role}`;
		message.textContent = text;
		chatLog.appendChild(message);

		// Auto-scroll to the latest message (mobile-friendly).
		chatLog.scrollTop = chatLog.scrollHeight;
	};

	const sendQuestion = async () => {
		const question = chatInput.value.trim();
		if (!question) {
			setStatus("Please type a question before sending.");
			return;
		}

		// Add user message to UI and memory.
		conversation.push({ role: "user", content: question });
		appendMessage("user", question);
		chatInput.value = "";

		// Show a friendly loading indicator.
		setStatus("Thinking…");

		try {
			const response = await fetch("http://localhost:8000/chat", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ question }),
			});

			if (!response.ok) {
				throw new Error(`Server error: ${response.status}`);
			}

			const data = await response.json();
			const answer = data.answer || "No response received.";

			conversation.push({ role: "assistant", content: answer });
			appendMessage("ai", answer);
			setStatus("");
		} catch (error) {
			// Friendly error messaging for network or server issues.
			setStatus("Sorry, the local AI service could not be reached. Please check that the backend is running.");
			appendMessage("ai", "I couldn’t reach the local advisory service. Please try again once the backend is running.");
			console.error(error);
		}
	};

	// Click to send
	chatSubmit.addEventListener("click", sendQuestion);

	// Enter key to send
	chatInput.addEventListener("keydown", (event) => {
		if (event.key === "Enter") {
			event.preventDefault();
			sendQuestion();
		}
	});
})();
