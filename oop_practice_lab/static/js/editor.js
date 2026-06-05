const starterCode = document.getElementById('starter-code');
const editorNode = document.getElementById('editor');
const form = document.getElementById('submission-form');
const statusNode = document.getElementById('submit-status');
let codeEditor;

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop().split(';').shift();
  }
  return '';
}

if (editorNode && window.require) {
  window.require.config({
    paths: {
      vs: 'https://cdnjs.cloudflare.com/ajax/libs/monaco-editor/0.44.0/min/vs',
    },
  });
  window.require(['vs/editor/editor.main'], () => {
    codeEditor = monaco.editor.create(editorNode, {
      value: starterCode ? starterCode.value : '',
      language: 'python',
      theme: 'vs-dark',
      automaticLayout: true,
      minimap: { enabled: false },
      fontSize: 15,
    });
  });
}

if (form) {
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    statusNode.textContent = 'Evaluating your AST structure...';
    const exerciseId = form.querySelector('[name="exercise"]').value;
    const code = codeEditor ? codeEditor.getValue() : starterCode.value;

    try {
      const response = await fetch('/api/submissions/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ exercise: exerciseId, code }),
      });
      const data = await response.json();
      if (!response.ok) {
        statusNode.textContent = 'Submission failed. Please review the form and try again.';
        return;
      }
      window.location.href = `/results/${data.id}/`;
    } catch (error) {
      statusNode.textContent = 'Network error while submitting. Please try again.';
    }
  });
}
