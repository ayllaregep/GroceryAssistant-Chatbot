document.addEventListener("DOMContentLoaded", () => {
  const inputField = document.getElementById("user-input");
  const sendButton = document.getElementById("send-btn");
  const chatContainer = document.getElementById("chatbox");

  // Function to add message to the chat
  function addToChat(message, sender) {
    const messageElement = document.createElement("div");
    messageElement.classList.add(
      sender === "user" ? "user-message" : "bot-message"
    );
    messageElement.innerHTML = message;
    chatContainer.appendChild(messageElement);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  // Function to handle user message
  async function handleUserMessage() {
    const message = inputField.value;
    let shouldExport = false;
    if (!message.trim()) return;

    addToChat(message, "user");
    inputField.value = "";
    if (message == 9) shouldExport = true;
    try {
      const formData = new FormData();
      formData.append("message", message);

      const response = await fetch("/process_message", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const botResponse = await response.json();
        if (!shouldExport) {
          addToChat(botResponse, "bot");

          if (botResponse.startsWith("Bot: What range should the shop be")) {
            sendUserLocationToBackend();
          }
        } else {
          createExport(botResponse);
        }
      } else {
        throw new Error("Failed to process user message");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  }

  function createExport(shoppingList) {
    let exportResult = { chat: collectChat(), ShoppingList: shoppingList };
    const jsonString = JSON.stringify(exportResult, null, 2);

    // Create a Blob from the JSON string
    const jsonBlob = new Blob([jsonString], { type: "application/json" });

    // Create a download link with the Blob
    const downloadLink = document.createElement("a");
    downloadLink.href = URL.createObjectURL(jsonBlob);
    downloadLink.download = "shopping_list.json";
    downloadLink.innerText = "Download your data";
    downloadLink.classList.add("bot-message");
    chatContainer.appendChild(downloadLink);
    chatContainer.scrollTop = chatContainer.scrollHeight;
  }

  function collectChat() {
    let messeges = [];
    let children = [].slice.call(chatContainer.getElementsByTagName("div"), 0);
    children.forEach((element) => {
      if (element.classList.contains("bot-message"))
        messeges.push({ message: element.innerHTML, sender: "bot" });
      else messeges.push({ message: element.innerHTML, sender: "user" });
    });
    return messeges;
  }

  // Function to get user location
  function getUserLocation() {
    return new Promise((resolve, reject) => {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            resolve({
              lat: position.coords.latitude,
              lng: position.coords.longitude,
            });
          },
          (error) => {
            reject(error);
          }
        );
      } else {
        reject(new Error("Geolocation is not supported by this browser."));
      }
    });
  }

  // Function to send user location to the backend
  async function sendUserLocationToBackend() {
    try {
      const location = await getUserLocation();
      const response = await fetch("/set_location", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(location),
      });

      if (!response.ok) {
        throw new Error("Failed to send location to the backend");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  }

  // Event listeners for input field and send button
  inputField.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      handleUserMessage();
    }
  });

  sendButton.addEventListener("click", handleUserMessage);

  // Initialize bot with a random greeting message and menu
  addToChat("Hello! I am your Grocery Assistant. Here's what I can do:", "bot");
  addToChat(
    `1. Show shopping list<br>
2. Add products to the list<br>
3. Remove products from the list<br>
4. Find nearby stores<br>
5. Suggest a recipe<br>
6. Check the total number of products in the list<br>
7. Check if a product is in the list<br>
8. Empty the shopping list<br>
9. Export the shopping list as a JSON file`,
    "bot"
  );
});
