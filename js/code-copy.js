document.addEventListener("DOMContentLoaded", () => {
  const snippets = document.querySelectorAll(".code-snippet[data-src]");

  snippets.forEach((snippet) => {
    const src = snippet.getAttribute("data-src");
    if (!src) {
      return;
    }

    fetch(src)
      .then((response) => {
        if (!response.ok) {
          throw new Error(`Failed to fetch ${src}: ${response.status}`);
        }
        return response.text();
      })
      .then((code) => {
        snippet.textContent = code;
        snippet.dataset.loaded = "true";
      })
      .catch((error) => {
        console.error(error);
        snippet.textContent = "# コードを読み込めませんでした";
        snippet.classList.add("code-load-error");
      });
  });

  const buttons = document.querySelectorAll(".copy-button[data-copy-target]");

  buttons.forEach((button) => {
    button.addEventListener("click", async () => {
      const targetId = button.getAttribute("data-copy-target");
      const codeBlock = document.getElementById(targetId);
      if (!codeBlock) {
        return;
      }

      const originalLabel = button.textContent;
      const codeText = codeBlock.textContent;

      try {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          await navigator.clipboard.writeText(codeText);
        } else {
          const fallbackArea = document.createElement("textarea");
          fallbackArea.value = codeText;
          fallbackArea.style.position = "fixed";
          fallbackArea.style.opacity = "0";
          document.body.appendChild(fallbackArea);
          fallbackArea.focus();
          fallbackArea.select();
          document.execCommand("copy");
          document.body.removeChild(fallbackArea);
        }

        button.textContent = "コピー済み";
        button.classList.add("copied");
        setTimeout(() => {
          button.textContent = originalLabel;
          button.classList.remove("copied");
        }, 2000);
      } catch (error) {
        console.error("Copy failed", error);
        button.textContent = "コピーできません";
        setTimeout(() => {
          button.textContent = originalLabel;
        }, 2000);
      }
    });
  });
});
